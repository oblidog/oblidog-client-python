from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True, slots=True)
class ObligationPeriod:
    """Calendar month identifying an obligation within the key-bound category.

    Args:
        year: Four-digit calendar year (1 through 9999).
        month: Calendar month (1 through 12).

    The integration API key supplies the category, so callers do not need to
    construct or retain an Oblidog obligation key.
    """

    year: int
    month: int

    def __post_init__(self) -> None:
        if not isinstance(self.year, int) or isinstance(self.year, bool):
            raise TypeError("year must be an integer")
        if not isinstance(self.month, int) or isinstance(self.month, bool):
            raise TypeError("month must be an integer")
        if not 1 <= self.year <= 9999:
            raise ValueError("year must be between 1 and 9999")
        if not 1 <= self.month <= 12:
            raise ValueError("month must be between 1 and 12")

    def __str__(self) -> str:
        """Return the API path representation in ``YYYY-MM`` format."""
        return f"{self.year:04d}-{self.month:02d}"
