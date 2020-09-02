from django.contrib import admin

from .models import Accounts, Transactions
# Register your models here.
admin.site.register(Accounts)
admin.site.register(Transactions)