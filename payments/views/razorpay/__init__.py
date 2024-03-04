import razorpay
from django.conf import settings

RAZORPAY_CLIENT = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
