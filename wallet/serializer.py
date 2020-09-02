from rest_framework import serializers
from .models import Accounts, Transactions

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Transactions
        fields = '__all__'
