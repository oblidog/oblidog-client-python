from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ObligationIntegrationUpdate")


@_attrs_define
class ObligationIntegrationUpdate:
    """Values an API-key authenticated integration may update.

    Attributes:
        current_amount (float | None | str | Unset):
        due_date (datetime.date | None | Unset):
        issue_date (datetime.date | None | Unset):
    """

    current_amount: float | None | str | Unset = UNSET
    due_date: datetime.date | None | Unset = UNSET
    issue_date: datetime.date | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        current_amount: float | None | str | Unset
        if isinstance(self.current_amount, Unset):
            current_amount = UNSET
        else:
            current_amount = self.current_amount

        due_date: None | str | Unset
        if isinstance(self.due_date, Unset):
            due_date = UNSET
        elif isinstance(self.due_date, datetime.date):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date

        issue_date: None | str | Unset
        if isinstance(self.issue_date, Unset):
            issue_date = UNSET
        elif isinstance(self.issue_date, datetime.date):
            issue_date = self.issue_date.isoformat()
        else:
            issue_date = self.issue_date

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if current_amount is not UNSET:
            field_dict["current_amount"] = current_amount
        if due_date is not UNSET:
            field_dict["due_date"] = due_date
        if issue_date is not UNSET:
            field_dict["issue_date"] = issue_date

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_current_amount(data: object) -> float | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | str | Unset, data)

        current_amount = _parse_current_amount(d.pop("current_amount", UNSET))

        def _parse_due_date(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                due_date_type_0 = datetime.date.fromisoformat(data)

                return due_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None | Unset, data)

        due_date = _parse_due_date(d.pop("due_date", UNSET))

        def _parse_issue_date(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                issue_date_type_0 = datetime.date.fromisoformat(data)

                return issue_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None | Unset, data)

        issue_date = _parse_issue_date(d.pop("issue_date", UNSET))

        obligation_integration_update = cls(
            current_amount=current_amount,
            due_date=due_date,
            issue_date=issue_date,
        )

        return obligation_integration_update
