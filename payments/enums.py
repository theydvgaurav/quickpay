from enum import Enum


class TransactionStatus(Enum):
    CREATED = 'created'
    CAPTURED = 'captured'
    FAILED = 'failed'
    REFUNDED = 'refunded'


class Currency(Enum):
    INR = 'INR'
    USD = 'USD'
