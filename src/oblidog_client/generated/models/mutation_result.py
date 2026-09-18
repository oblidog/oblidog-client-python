from enum import Enum


class MutationResult(str, Enum):
    CREATED = "created"
    UNCHANGED = "unchanged"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
