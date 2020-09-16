from django.urls import path
from .views import AccountAPIView, TransactionAPIView
from . import views

app_name='wallet'
urlpatterns = [
    path('', AccountAPIView.as_view(), name='home'),
    path('transactions/', TransactionAPIView.as_view(), name='transactions'),
]