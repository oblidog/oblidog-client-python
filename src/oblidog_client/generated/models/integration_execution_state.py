from enum import Enum


class IntegrationExecutionState(str, Enum):
    FINISHED = "finished"
    NEVER_RUN = "never_run"
    RUNNING = "running"
    TIMED_OUT = "timed_out"

    def __str__(self) -> str:
        return str(self.value)
