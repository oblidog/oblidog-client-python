from enum import Enum


class CurrentValueSource(str, Enum):
    AUTOMATIC = "automatic"
    INTEGRATION = "integration"
    LEGACY = "legacy"
    MANUAL = "manual"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
