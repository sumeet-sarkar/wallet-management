from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
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

from wallet.models import Accounts, Transactions

from wallet.serializer import AccountsSerializer, TransactionsSerializer

from django.views import generic

# Create your views here.

class AccountAPIView(APIView):

    def getAccounts(self, id=None):
        if(id == None):
            return Accounts.objects.all()
        else:
            return Accounts.objects.filter(id=id)

    def updateAccounts(self, id, newAmount, oldAmount = 0):
        account = (self.getAccounts(id))[0]
        amount = account.currentBalance - newAmount + oldAmount
        if amount >= 0:
            account.currentBalance = amount
            account.lastModified = timezone.now()
            account.save()
            return amount
        return False

    def get(self, request):
        account = self.getAccounts(request.GET.get("id"))
        serializer = AccountsSerializer(account, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionsAPIView(APIView):

    def getAllTransactions(self, id=None):
        if(id == None):
            return Transactions.objects.all().order_by('createdOn')[:15]
        else:
            account = Accounts.objects.get(id=id)
            return Transactions.objects.filter(accountNumber=account)

    def getTransaction(self, id=None):
        if(id == None):
            return Transactions.objects.all().order_by('createdOn')[:15]
        else:
            return Transactions.objects.filter(id=id)

    def getClosingBalance(self, accountId, newAmountSpent, oldAmountSpent = 0):
        account = AccountAPIView()
        closingBalance = account.updateAccounts(accountId, newAmountSpent, oldAmountSpent)
        return closingBalance

    def updateAllTransactions(self, transaction, amount):
        with TRANSACTION.atomic():
            transactions = Transactions.objects.filter(date__gt=transaction.date)
            for i in transactions:
                i.closingBalance += amount
                i.lastModified = timezone.now()
                i.save()
            return True

    def get(self, request):
        transaction = self.getAllTransactions(request.GET.get("accountid"))
        serializer = TransactionsSerializer(transaction, many=True)
        return Response(serializer.data)

    def post(self, request):
        closingBalance = self.getClosingBalance(request.data["accountNumber"], request.data["amountSpent"])
        
        if closingBalance:
            request.data["closingBalance"] = closingBalance
            serializer = TransactionsSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("not enough balance", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        transaction = (self.getTransaction(id=request.data["id"]))[0]
        closingBalance = self.getClosingBalance(request.data["accountNumber"], request.data["amountSpent"], transaction.amountSpent)
        if closingBalance:
            amount = transaction.amountSpent - request.data["amountSpent"]
            flag = self.updateAllTransactions(transaction, amount)
            if flag:
                request.data["closingBalance"] = transaction.closingBalance + amount
                request.data["lastModified"] = timezone.now()

                serializer = TransactionsSerializer(transaction, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("not enough balance", status=status.HTTP_400_BAD_REQUEST)