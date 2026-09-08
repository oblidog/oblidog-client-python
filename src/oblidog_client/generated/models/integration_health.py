from enum import Enum


class IntegrationHealth(str, Enum):
    DISABLED = "disabled"
    ERROR = "error"
    HEALTHY = "healthy"
    NEVER_RUN = "never_run"
    RUNNING = "running"
    STALE = "stale"
    TIMED_OUT = "timed_out"

    def __str__(self) -> str:
        return str(self.value)
