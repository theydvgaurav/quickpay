import os

import razorpay

RAZORPAY_CLIENT = razorpay.Client(auth=(os.getenv('RAZORPAY_API_KEY'), os.getenv('RAZORPAY_API_SECRET')))
