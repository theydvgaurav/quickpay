from django.urls import path

from .views.payment_status import TransactionStatusView
from .views.razorpay.initiate import RazorpayTransactionInitiationView

urlpatterns = [
    path('razorpay/initiate/', RazorpayTransactionInitiationView.as_view(), name='one-time-razorpay-initiate'),
    path('transaction/<str:id>/status/', TransactionStatusView.as_view(), name='transaction-status')
]
