from django.db import models
from django.utils import timezone

# Create your models here.
class Accounts(models.Model):
    class Banks(models.TextChoices):
        UBI  = "UBI"
        SBI  = "SBI"
        HDFC = "HDFC"
        IOB  = "IOB"

    accountNumber   = models.CharField(max_length=12)
    bankName        = models.CharField(max_length= 40,choices = Banks.choices)
    currentBalance  = models.FloatField()
    email           = models.EmailField(max_length=30)
    phone           = models.IntegerField()
    createdOn       = models.DateTimeField('created date', default=timezone.now)
    lastModified    = models.DateTimeField('modified date',default=timezone.now)
    isDeleted       = models.BooleanField(default=False)

class Transactions(models.Model):

    accountNumber  = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    amountSpent    = models.FloatField()
    closingBalance = models.FloatField(default=None)
    reason         = models.CharField(max_length=40)
    date           = models.DateTimeField(default=timezone.now)
    createdOn      = models.DateTimeField('created date', default=timezone.now)
    lastModified   = models.DateTimeField('modified date', default=timezone.now)
    isDeleted      = models.BooleanField(default=False)