from django.urls import path
from .views import AccountAPIView, TransactionsAPIView
from . import views

app_name='wallet'
urlpatterns = [
    path('', AccountAPIView.as_view(), name='home'),
    path('transactions/', TransactionsAPIView.as_view(), name='transactions'),
]