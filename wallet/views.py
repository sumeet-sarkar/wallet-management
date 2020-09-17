from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, Http404
from rest_framework import serializers
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction as TRANSACTION
from .messages import *

from wallet.models import Account, Transaction

from wallet.serializer import AccountSerializer, TransactionSerializer

from django.views import generic

class AccountAPIView(APIView):

    def __init__(self):
        self.accounts = None

    def getAccounts(self, querySet):
        self.accounts = Account.objects.all()

        id = querySet.get('id', None)
        phone = querySet.get('phone', None)
        accountNumber = querySet.get('accountNumber', None)
        bankName = querySet.get('bankName', None)

        if (id != None):
            self.accounts = self.accounts.filter(id=id)
        if (phone != None):
            self.accounts = self.accounts.filter(phone=phone)
        if (accountNumber != None):
            self.accounts = self.accounts.filter(accountNumber=accountNumber)
        if (bankName != None):
            self.accounts = self.accounts.filter(bankName=bankName)

        if len(self.accounts) == 0:
            return NO_SUCH_ACCOUNT_FOUND
        return True

    def updateAccount(self, id, newAmount, oldAmount = 0):
        account = self.getAccounts(id)
        if account:
            amount = account.currentBalance - newAmount + oldAmount
            if amount >= 0:
                account.currentBalance = amount
                account.lastModified = timezone.now()
                account.save()
                return amount
            return NOT_ENOUGH_BALANCE

        return NO_SUCH_ACCOUNT_FOUND

    def get(self, request):
        statusMessage = self.getAccounts(request.query_params)
        if statusMessage == True:
            serializer = AccountSerializer(self.accounts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(statusMessage, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        querySet = {"accountNumber": request.data["accountNumber"]}

        #checking if duplicate
        statusMessage = self.getAccounts(querySet)
        if statusMessage == True:
            return Response(DUPLICATE_ACCOUNT, status=status.HTTP_400_BAD_REQUEST)

        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        statusMessage = self.getAccounts(request.query_params)
        if statusMessage == True:
            transactions = TransactionAPIView()
            # account in model.Transaction is id in model.Account
            # statusMessageTransactions unused variable because existing method is reused
            statusMessageTransactions = transactions.getTransactions( {"account": self.accounts[0].id} )
            with TRANSACTION.atomic():
                for transaction in transactions.transactions:
                    transaction.isDeleted = True
                    transaction.lastModified = timezone.now()
                    transaction.save()
                data = {
                    "lastModified": timezone.now(),
                    "isDeleted": True
                }

                serializer = AccountSerializer(self.accounts[0], data=data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(statusMessage, status=status.HTTP_404_NOT_FOUND)

class TransactionAPIView(APIView):

    def __init__(self):
        self.closingBalance = None
        self.account = None
        self.transactions = None

    def getAccount(self, querySet):
        accountObj = AccountAPIView()
        statusMessage = accountObj.getAccounts(querySet)
        if statusMessage != True:
            return statusMessage
        self.account = accountObj.accounts[0]
        return statusMessage

    def updateAccount(self, closingBalance):
        self.account.currentBalance = closingBalance
        self.account.lastModified = timezone.now()
        self.account.save()

    def getTransactions(self, querySet):
        self.transactions = Transaction.objects.all()

        id = querySet.get('id', None)
        date = querySet.get('date', None)
        account = querySet.get('account', None)

        if (id != None):
            self.transactions = self.transactions.filter(id=id)
        if (date != None):
            self.transactions = self.transactions.filter(date=date)
        if (account != None):
            #account in model.Transaction is id in model.Account
            query = {'id': account}
            statusMessage = self.getAccount(query)

            if statusMessage != True:
                return statusMessage
            self.transactions = self.transactions.filter(account=self.account)

        if len(self.transactions) == 0:
            return NO_SUCH_TRANSACTION_FOUND
        return True

    def getClosingBalance(self, newAmount, oldAmount = 0):
        closingBalance = self.account.currentBalance + newAmount - oldAmount
        if closingBalance >= 0:
            return True, closingBalance
        return NOT_ENOUGH_BALANCE, None

    def updateAllTransactions(self, amount):
        with TRANSACTION.atomic():
            transactions = Transaction.objects.filter(date__gt=self.transactions[0].date)
            for i in transactions:
                i.closingBalance -= amount
                i.lastModified = timezone.now()
                i.save()
            return True
        return OPERATION_INCOMPLETE

    def get(self, request):
        statusMessage = self.getTransactions(request.query_params)

        if statusMessage == True:
            serializer = TransactionSerializer(self.transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(statusMessage, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        querySet = {"id": request.data["account"]}
        statusMessage = self.getAccount(querySet)
        
        if statusMessage == True:
            statusMessageClosingBalance, closingBalance = self.getClosingBalance(request.data["amount"])

            if statusMessageClosingBalance == True:
                self.updateAccount(closingBalance)
                request.data["closingBalance"] = closingBalance
                serializer = TransactionSerializer(data = request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(statusMessageClosingBalance, status=status.HTTP_400_BAD_REQUEST)

        return Response(statusMessage, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        querySet = {"id": request.data["id"]}
        statusMessage = self.getTransactions(querySet)

        if statusMessage == True:
            self.account = self.transactions[0].account
            statusMessageClosingBalance, closingBalance = self.getClosingBalance(request.data["amount"], self.transactions[0].amount)

            if statusMessageClosingBalance == True:
                self.updateAccount(closingBalance)
                amount = self.transactions[0].amount - request.data["amount"]
                flag = self.updateAllTransactions(amount)

                if flag == True:
                    request.data["closingBalance"] = self.transactions[0].closingBalance - amount
                    request.data["lastModified"] = timezone.now()

                    serializer = TransactionSerializer(self.transactions[0], data=request.data, partial=True)

                    if serializer.is_valid():
                        serializer.save()
                        return Response(status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(flag, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(statusMessageClosingBalance, status=status.HTTP_400_BAD_REQUEST)

        return Response(statusMessage, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        statusMessage = self.getTransactions(request.query_params)

        if statusMessage == True:
            self.account = self.transactions[0].account
            statusMessageClosingBalance, closingBalance = self.getClosingBalance(0, self.transactions[0].amount)

            if statusMessageClosingBalance == True:
                self.updateAccount(closingBalance)
                flag = self.updateAllTransactions(self.transactions[0].amount)

                if flag:
                    data = {
                        "lastModified": timezone.now(),
                        "isDeleted": True
                    }
                    serializer = TransactionSerializer(self.transactions[0], data=data, partial=True)

                    if serializer.is_valid():
                        serializer.save()
                        return Response(status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(flag, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(statusMessageClosingBalance, status=status.HTTP_400_BAD_REQUEST)

        return Response(statusMessage, status=status.HTTP_404_NOT_FOUND)
