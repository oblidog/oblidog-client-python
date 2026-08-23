from enum import Enum


class EffectiveValueSourceMode(str, Enum):
    AUTOMATIC = "automatic"
    INTEGRATION = "integration"
    LEGACY = "legacy"
    MANUAL = "manual"
    MIXED = "mixed"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
