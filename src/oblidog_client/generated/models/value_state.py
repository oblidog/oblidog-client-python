from enum import Enum


class ValueState(str, Enum):
    CONFIRMED = "confirmed"
    ESTIMATED = "estimated"
    OVERRIDDEN = "overridden"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
