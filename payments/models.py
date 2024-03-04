from uuid import uuid4

from django.db import models
from enumfields import EnumField

from base.model import ApplicationBaseModel
from payments.enums import TransactionStatus, Currency
from users.models import User


class Transaction(ApplicationBaseModel):
    transaction_id = models.UUIDField(primary_key=True, default=uuid4)
    payment_id = models.CharField(max_length=255, unique=True, null=True)
    group_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    status = EnumField(TransactionStatus, max_length=64, protected=True, default=TransactionStatus.CREATED)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    currency = EnumField(Currency)
