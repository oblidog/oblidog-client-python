from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.current_value_source import CurrentValueSource
from ..models.effective_value_source_mode import EffectiveValueSourceMode
from ..models.obligation_lifecycle import ObligationLifecycle
from ..models.value_state import ValueState

if TYPE_CHECKING:
    from ..models.obligation_period_public import ObligationPeriodPublic


T = TypeVar("T", bound="ObligationPublic")


@_attrs_define
class ObligationPublic:
    """
    Attributes:
        amount_source (CurrentValueSource):
        amount_state (ValueState):
        category_code (str):
        category_id (UUID):
        created_at (datetime.datetime):
        currency (None | str):
        current_amount (None | str):
        due_date (datetime.date | None):
        due_date_source (CurrentValueSource):
        due_date_state (ValueState):
        effective_value_source (EffectiveValueSourceMode):
        id (UUID):
        issue_date (datetime.date | None):
        issue_date_source (CurrentValueSource):
        issue_date_state (ValueState):
        key (str):
        ledger_id (UUID):
        lifecycle (ObligationLifecycle):
        name (str):
        notes (None | str):
        paid_at (datetime.datetime | None):
        period (ObligationPeriodPublic):
        updated_at (datetime.datetime):
    """

    amount_source: CurrentValueSource
    amount_state: ValueState
    category_code: str
    category_id: UUID
    created_at: datetime.datetime
    currency: None | str
    current_amount: None | str
    due_date: datetime.date | None
    due_date_source: CurrentValueSource
    due_date_state: ValueState
    effective_value_source: EffectiveValueSourceMode
    id: UUID
    issue_date: datetime.date | None
    issue_date_source: CurrentValueSource
    issue_date_state: ValueState
    key: str
    ledger_id: UUID
    lifecycle: ObligationLifecycle
    name: str
    notes: None | str
    paid_at: datetime.datetime | None
    period: ObligationPeriodPublic
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_source = self.amount_source.value

        amount_state = self.amount_state.value

        category_code = self.category_code

        category_id = str(self.category_id)

        created_at = self.created_at.isoformat()

        currency: None | str
        currency = self.currency

        current_amount: None | str
        current_amount = self.current_amount

        due_date: None | str
        if isinstance(self.due_date, datetime.date):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date

        due_date_source = self.due_date_source.value

        due_date_state = self.due_date_state.value

        effective_value_source = self.effective_value_source.value

        id = str(self.id)

        issue_date: None | str
        if isinstance(self.issue_date, datetime.date):
            issue_date = self.issue_date.isoformat()
        else:
            issue_date = self.issue_date

        issue_date_source = self.issue_date_source.value

        issue_date_state = self.issue_date_state.value

        key = self.key

        ledger_id = str(self.ledger_id)

        lifecycle = self.lifecycle.value

        name = self.name

        notes: None | str
        notes = self.notes

        paid_at: None | str
        if isinstance(self.paid_at, datetime.datetime):
            paid_at = self.paid_at.isoformat()
        else:
            paid_at = self.paid_at

        period = self.period.to_dict()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount_source": amount_source,
                "amount_state": amount_state,
                "category_code": category_code,
                "category_id": category_id,
                "created_at": created_at,
                "currency": currency,
                "current_amount": current_amount,
                "due_date": due_date,
                "due_date_source": due_date_source,
                "due_date_state": due_date_state,
                "effective_value_source": effective_value_source,
                "id": id,
                "issue_date": issue_date,
                "issue_date_source": issue_date_source,
                "issue_date_state": issue_date_state,
                "key": key,
                "ledger_id": ledger_id,
                "lifecycle": lifecycle,
                "name": name,
                "notes": notes,
                "paid_at": paid_at,
                "period": period,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.obligation_period_public import ObligationPeriodPublic

        d = dict(src_dict)
        amount_source = CurrentValueSource(d.pop("amount_source"))

        amount_state = ValueState(d.pop("amount_state"))

        category_code = d.pop("category_code")

        category_id = UUID(d.pop("category_id"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_currency(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        currency = _parse_currency(d.pop("currency"))

        def _parse_current_amount(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        current_amount = _parse_current_amount(d.pop("current_amount"))

        def _parse_due_date(data: object) -> datetime.date | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                due_date_type_0 = datetime.date.fromisoformat(data)

                return due_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None, data)

        due_date = _parse_due_date(d.pop("due_date"))

        due_date_source = CurrentValueSource(d.pop("due_date_source"))

        due_date_state = ValueState(d.pop("due_date_state"))

        effective_value_source = EffectiveValueSourceMode(
            d.pop("effective_value_source")
        )

        id = UUID(d.pop("id"))

        def _parse_issue_date(data: object) -> datetime.date | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                issue_date_type_0 = datetime.date.fromisoformat(data)

                return issue_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None, data)

        issue_date = _parse_issue_date(d.pop("issue_date"))

        issue_date_source = CurrentValueSource(d.pop("issue_date_source"))

        issue_date_state = ValueState(d.pop("issue_date_state"))

        key = d.pop("key")

        ledger_id = UUID(d.pop("ledger_id"))

        lifecycle = ObligationLifecycle(d.pop("lifecycle"))

        name = d.pop("name")

        def _parse_notes(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        notes = _parse_notes(d.pop("notes"))

        def _parse_paid_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                paid_at_type_0 = datetime.datetime.fromisoformat(data)

                return paid_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        paid_at = _parse_paid_at(d.pop("paid_at"))

        period = ObligationPeriodPublic.from_dict(d.pop("period"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        obligation_public = cls(
            amount_source=amount_source,
            amount_state=amount_state,
            category_code=category_code,
            category_id=category_id,
            created_at=created_at,
            currency=currency,
            current_amount=current_amount,
            due_date=due_date,
            due_date_source=due_date_source,
            due_date_state=due_date_state,
            effective_value_source=effective_value_source,
            id=id,
            issue_date=issue_date,
            issue_date_source=issue_date_source,
            issue_date_state=issue_date_state,
            key=key,
            ledger_id=ledger_id,
            lifecycle=lifecycle,
            name=name,
            notes=notes,
            paid_at=paid_at,
            period=period,
            updated_at=updated_at,
        )

        obligation_public.additional_properties = d
        return obligation_public

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
