import logging

from base.views import ApplicationBaseAPIView
from exceptions import APIException
from middlewares.quickpay_user import QuickPayUserAuthentication
from payments.models import Transaction

logger = logging.getLogger(__name__)


class TransactionStatusView(ApplicationBaseAPIView):
    authentication_classes = [QuickPayUserAuthentication]

    def get(self, request, *args, **kwargs):
        transaction_id = kwargs.get('id')
        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Exception as e:
            raise APIException(message='Invalid Transaction', status_code=400)
        return self.get_response(
            data={"transactionId": str(transaction.transaction_id), "status": transaction.status.value})
