from enum import Enum


class IntegrationConflictCode(str, Enum):
    DUPLICATE_KEY = "duplicate_key"
    INTEGRATION_DISABLED = "integration_disabled"
    REVISION_CONFLICT = "revision_conflict"
    RUN_CONFLICT = "run_conflict"
    RUN_IN_PROGRESS = "run_in_progress"

    def __str__(self) -> str:
        return str(self.value)
