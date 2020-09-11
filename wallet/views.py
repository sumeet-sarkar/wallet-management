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

from wallet.models import Accounts, Transactions

from wallet.serializer import AccountsSerializer, TransactionsSerializer

from django.views import generic

class AccountAPIView(APIView):

    def __init__(self):
        self.accounts = None

    def getAccounts(self, querySet):
        self.accounts = Accounts.objects.all()

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
            serializer = AccountsSerializer(self.accounts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(statusMessage, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        querySet = {"accountNumber": request.data["accountNumber"]}

        #checking if duplicate
        statusMessage = self.getAccounts(querySet)
        if statusMessage == True:
            return Response(DUPLICATE_ACCOUNT, status=status.HTTP_400_BAD_REQUEST)

        serializer = AccountsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionsAPIView(APIView):

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
        self.transactions = Transactions.objects.all()

        id = querySet.get('id', None)
        date = querySet.get('date', None)
        accountNumber = querySet.get('accountNumber', None)

        if (id != None):
            self.transactions = self.transactions.filter(id=id)
        if (date != None):
            self.transactions = self.transactions.filter(date=date)
        if (accountNumber != None):
            query = {'accountNumber': accountNumber}
            statusMessage = self.getAccount(query)
            if statusMessage != True:
                return statusMessage
            self.transactions = self.transactions.filter(accountNumber=self.account)

        if len(self.transactions) == 0:
            return NO_SUCH_TRANSACTION_FOUND
        return True

    def getClosingBalance(self, accountNumber, newAmountSpent, oldAmountSpent = 0):
        querySet = {"accountNumber": accountNumber}
        statusMessage = self.getAccount(querySet)
        if statusMessage == True:
            closingBalance = self.account.currentBalance - newAmountSpent + oldAmountSpent
            if closingBalance >= 0:
                return True, closingBalance
            return NOT_ENOUGH_BALANCE, None
        return statusMessage, None

    def updateAllTransactions(self, amount):
        with TRANSACTION.atomic():
            transactions = Transactions.objects.filter(date__gt=self.transactions[0].date)
            for i in transactions:
                i.closingBalance += amount
                i.lastModified = timezone.now()
                i.save()
            return True

    def get(self, request):
        statusMessage = self.getTransactions(request.query_params)
        if statusMessage == True:
            serializer = TransactionsSerializer(self.transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(statusMessage, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        statusMessage, closingBalance = self.getClosingBalance(request.data["accountNumber"], request.data["amountSpent"])
        if statusMessage == True:
            self.updateAccount(closingBalance)
            request.data["closingBalance"] = closingBalance
            request.data["accountNumber"] = self.account.pk
            serializer = TransactionsSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(statusMessage, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        querySet = {"id": request.data["id"]}
        statusMessage = self.getTransactions(querySet)

        if statusMessage == True:
            statusMessageClosingBalance, closingBalance = self.getClosingBalance(request.data["accountNumber"], request.data["amountSpent"], self.transactions[0].amountSpent)
            if statusMessageClosingBalance == True:
                self.updateAccount(closingBalance)
                amount = self.transactions[0].amountSpent - request.data["amountSpent"]
                flag = self.updateAllTransactions(amount)
                if flag:
                    request.data["closingBalance"] = self.transactions[0].closingBalance + amount
                    request.data["lastModified"] = timezone.now()
                    request.data["accountNumber"] = self.transactions[0].accountNumber.id

                    serializer = TransactionsSerializer(self.transactions[0], data=request.data, partial=True)

                    if serializer.is_valid():
                        serializer.save()
                        return Response(status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(statusMessageClosingBalance, status=status.HTTP_400_BAD_REQUEST)
        return Response(statusMessage, status=status.HTTP_400_BAD_REQUEST)
