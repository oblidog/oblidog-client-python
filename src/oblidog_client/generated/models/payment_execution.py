from enum import Enum


class PaymentExecution(str, Enum):
    AUTOMATIC_COLLECTION = "automatic_collection"
    SCHEDULED_TRANSFER = "scheduled_transfer"

    def __str__(self) -> str:
        return str(self.value)
