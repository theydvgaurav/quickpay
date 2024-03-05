import logging

from base.views import ApplicationBaseAPIView
from middlewares.quickpay_user import QuickPayUserAuthentication
from payments.models import Transaction
from . import RAZORPAY_CLIENT
from ...enums import Currency

logger = logging.getLogger(__name__)


class RazorpayTransactionInitiationView(ApplicationBaseAPIView):
    authentication_classes = [QuickPayUserAuthentication]

    def post(self, request, *args, **kwargs):
        amount = request.data.get('amount')

        transaction = Transaction(
            user=self.request.user,
            amount=amount,
            currency=Currency.INR,
        )

        try:
            order = RAZORPAY_CLIENT.order.create(data={
                'amount': int(transaction.amount * 100),
                'currency': Currency.INR.value,
                'receipt': str(transaction.transaction_id),
                'payment_capture': 1,
                'notes': {}
            })
            transaction.group_id = order['id']
            transaction.save(force_insert=True)

            return self.get_response(data={
                'order_id': order['id'],
                'transaction_id': str(transaction.transaction_id)
            })
        except Exception as e:
            logger.error(f"{e} Exception occurred while creating transaction {transaction.transaction_id}")
            return self.get_response()
