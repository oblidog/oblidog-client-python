class FindogError(Exception):
    """Base exception raised by the high-level Findog client."""


class FindogApiError(FindogError):
    """The Findog API returned an unexpected response."""

    def __init__(self, status_code: int, content: bytes = b"") -> None:
        self.status_code = status_code
        self.content = content
        detail = content.decode(errors="replace") if content else ""
        message = f"Findog API returned HTTP {status_code}"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message)


class FindogValidationError(FindogError):
    """The Findog API rejected request parameters or payload."""
