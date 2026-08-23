from enum import Enum


class ObligationLifecycle(str, Enum):
    CANCELED = "canceled"
    COLLECTING_DATA = "collecting_data"
    DRAFT = "draft"
    ERROR = "error"
    PAID = "paid"
    READY = "ready"

    def __str__(self) -> str:
        return str(self.value)
