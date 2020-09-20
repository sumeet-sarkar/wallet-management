from rest_framework import status
from rest_framework.test import APITestCase
from wallet.models import Account, Transaction
from wallet.messages import *


class AccountTests(APITestCase):
    def setUp(self):
        Account.objects.create(
            accountNumber= "123456789",
            bank= "UBI",
            currentBalance= 100,
            email= "sumeet.somu@gmail.com",
            phone= 44
        )

    def testGetAccount(self):

        """
        GET method for accounts
        """

        url = "http://localhost:8000/wallet/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = "http://localhost:8000/wallet/?id=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = "http://localhost:8000/wallet/?id=12"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Eg value of response.content is b'"No such Account found."'
        # Eg value of response.content.decode("utf-8") is "No such Account found." (with the double quote)
        self.assertEqual(response.content.decode("utf-8").strip('"'), NO_SUCH_ACCOUNT_FOUND)

    def testPostAccountSuccessful(self):

        """
        successful POST method for accounts 
        """

        data = {
            "accountNumber": "1234567",
            "bank": "UBI",
            "currentBalance": 100,
            "email": "sumeet.somu@gmail.com",
            "phone": 44
        }

        url = "http://localhost:8000/wallet/"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(response.content.decode("utf-8").strip('"'), DUPLICATE_ACCOUNT)

    def testDeleteAccount(self):

        """
        Delete method for account
        """

        url = "http://localhost:8000/wallet/?id=1"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.get(pk=1).isDeleted, True)

        url = "http://localhost:8000/wallet/?id=2"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content.decode("utf-8").strip('"'), NO_SUCH_ACCOUNT_FOUND)

class TransactionTests(APITestCase):
    def setUp(self):
        Account.objects.create(
            accountNumber= "123456789",
            bank= "UBI",
            currentBalance= 100,
            email= "sumeet.somu@gmail.com",
            phone= 44
        )

        self.account = Account.objects.get(accountNumber="123456789")

        Transaction.objects.create(
            account = self.account,
            amount = 100,
            reason = "test",
            closingBalance = 0,
            isCredited = False
        )

    def testGetTransaction(self):

        """
        GET method for transactions
        """

        url = "http://localhost:8000/wallet/transactions/?account=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = "http://localhost:8000/wallet/transactions/?id=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = "http://localhost:8000/wallet/transactions/?account=12"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content.decode("utf-8").strip('"'), NO_SUCH_ACCOUNT_FOUND)
        

        url = "http://localhost:8000/wallet/transactions/?id=11"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content.decode("utf-8").strip('"'), NO_SUCH_TRANSACTION_FOUND)

    def testPostTransaction(self):

        """
        Post method for transactions
        """

        url = "http://localhost:8000/wallet/transactions/"
        data = {
            "account": self.account.pk,
            "amount": 10,
            "reason": "test",
            "isCredited": "False"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get(pk=1).currentBalance, 110)

        data["amount"] = -200
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content.decode("utf-8").strip('"'), NOT_ENOUGH_BALANCE)

        data["account"] = "123"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content.decode("utf-8").strip('"'), NO_SUCH_ACCOUNT_FOUND)

    def testPutTransaction(self):

        """
        Put method for transactions
        """

        url = "http://localhost:8000/wallet/transactions/"

        data = {
            "account": self.account.pk,
            "amount": 10,
            "reason": "test",
            "isCredited": "False"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get(pk=1).currentBalance, 110)

        data["amount"] = 5
        data["id"] = 2
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.get(pk=1).currentBalance, 105)

        data["amount"] = -1000
        data["id"] = 2
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.get(pk=1).currentBalance, 105)
        self.assertEqual(response.content.decode("utf-8").strip('"'), NOT_ENOUGH_BALANCE)

        data["id"] = 23
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content.decode("utf-8").strip('"'), NO_SUCH_TRANSACTION_FOUND)

    def testDeleteTransaction(self):

        """
        Delete method for transactions
        """

        url = "http://localhost:8000/wallet/transactions/"
        data = {
            "account": self.account.pk,
            "amount": 1000,
            "reason": "test",
            "isCredited": "False"
        }

        self.client.post(url, data)
        data["amount"] = -1000
        self.client.post(url, data)

        url = "http://localhost:8000/wallet/transactions/?id=1"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.get(pk=1).isDeleted, True)

        url = "http://localhost:8000/wallet/transactions/?id=2"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content.decode("utf-8").strip('"'), NOT_ENOUGH_BALANCE)

        url = "http://localhost:8000/wallet/transactions/?id=123"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content.decode("utf-8").strip('"'), NO_SUCH_TRANSACTION_FOUND)
