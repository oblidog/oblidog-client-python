from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.integration_execution_state import IntegrationExecutionState
from ..models.integration_health import IntegrationHealth
from ..models.integration_result import IntegrationResult

T = TypeVar("T", bound="IntegrationPublic")


@_attrs_define
class IntegrationPublic:
    """
    Attributes:
        category_ids (list[UUID]):
        created_at (datetime.datetime):
        current_deadline_at (datetime.datetime | None):
        current_finished_at (datetime.datetime | None):
        current_run_id (None | UUID):
        current_started_at (datetime.datetime | None):
        enabled (bool):
        enabled_at (datetime.datetime | None):
        execution_state (IntegrationExecutionState):
        health (IntegrationHealth):
        id (UUID):
        is_stale (bool):
        key (str):
        last_changes_detected (bool | None):
        last_error_code (None | str):
        last_error_message (None | str):
        last_finished_at (datetime.datetime | None):
        last_result (IntegrationResult | None):
        last_success_at (datetime.datetime | None):
        ledger_id (UUID):
        name (str):
        provider (str):
        revision (int):
        run_timeout_seconds (int):
        stale_after_seconds (int):
        updated_at (datetime.datetime):
    """

    category_ids: list[UUID]
    created_at: datetime.datetime
    current_deadline_at: datetime.datetime | None
    current_finished_at: datetime.datetime | None
    current_run_id: None | UUID
    current_started_at: datetime.datetime | None
    enabled: bool
    enabled_at: datetime.datetime | None
    execution_state: IntegrationExecutionState
    health: IntegrationHealth
    id: UUID
    is_stale: bool
    key: str
    last_changes_detected: bool | None
    last_error_code: None | str
    last_error_message: None | str
    last_finished_at: datetime.datetime | None
    last_result: IntegrationResult | None
    last_success_at: datetime.datetime | None
    ledger_id: UUID
    name: str
    provider: str
    revision: int
    run_timeout_seconds: int
    stale_after_seconds: int
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        category_ids = []
        for category_ids_item_data in self.category_ids:
            category_ids_item = str(category_ids_item_data)
            category_ids.append(category_ids_item)

        created_at = self.created_at.isoformat()

        current_deadline_at: None | str
        if isinstance(self.current_deadline_at, datetime.datetime):
            current_deadline_at = self.current_deadline_at.isoformat()
        else:
            current_deadline_at = self.current_deadline_at

        current_finished_at: None | str
        if isinstance(self.current_finished_at, datetime.datetime):
            current_finished_at = self.current_finished_at.isoformat()
        else:
            current_finished_at = self.current_finished_at

        current_run_id: None | str
        if isinstance(self.current_run_id, UUID):
            current_run_id = str(self.current_run_id)
        else:
            current_run_id = self.current_run_id

        current_started_at: None | str
        if isinstance(self.current_started_at, datetime.datetime):
            current_started_at = self.current_started_at.isoformat()
        else:
            current_started_at = self.current_started_at

        enabled = self.enabled

        enabled_at: None | str
        if isinstance(self.enabled_at, datetime.datetime):
            enabled_at = self.enabled_at.isoformat()
        else:
            enabled_at = self.enabled_at

        execution_state = self.execution_state.value

        health = self.health.value

        id = str(self.id)

        is_stale = self.is_stale

        key = self.key

        last_changes_detected: bool | None
        last_changes_detected = self.last_changes_detected

        last_error_code: None | str
        last_error_code = self.last_error_code

        last_error_message: None | str
        last_error_message = self.last_error_message

        last_finished_at: None | str
        if isinstance(self.last_finished_at, datetime.datetime):
            last_finished_at = self.last_finished_at.isoformat()
        else:
            last_finished_at = self.last_finished_at

        last_result: None | str
        if isinstance(self.last_result, IntegrationResult):
            last_result = self.last_result.value
        else:
            last_result = self.last_result

        last_success_at: None | str
        if isinstance(self.last_success_at, datetime.datetime):
            last_success_at = self.last_success_at.isoformat()
        else:
            last_success_at = self.last_success_at

        ledger_id = str(self.ledger_id)

        name = self.name

        provider = self.provider

        revision = self.revision

        run_timeout_seconds = self.run_timeout_seconds

        stale_after_seconds = self.stale_after_seconds

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "category_ids": category_ids,
                "created_at": created_at,
                "current_deadline_at": current_deadline_at,
                "current_finished_at": current_finished_at,
                "current_run_id": current_run_id,
                "current_started_at": current_started_at,
                "enabled": enabled,
                "enabled_at": enabled_at,
                "execution_state": execution_state,
                "health": health,
                "id": id,
                "is_stale": is_stale,
                "key": key,
                "last_changes_detected": last_changes_detected,
                "last_error_code": last_error_code,
                "last_error_message": last_error_message,
                "last_finished_at": last_finished_at,
                "last_result": last_result,
                "last_success_at": last_success_at,
                "ledger_id": ledger_id,
                "name": name,
                "provider": provider,
                "revision": revision,
                "run_timeout_seconds": run_timeout_seconds,
                "stale_after_seconds": stale_after_seconds,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        category_ids = []
        _category_ids = d.pop("category_ids")
        for category_ids_item_data in _category_ids:
            category_ids_item = UUID(category_ids_item_data)

            category_ids.append(category_ids_item)

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_current_deadline_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                current_deadline_at_type_0 = datetime.datetime.fromisoformat(data)

                return current_deadline_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        current_deadline_at = _parse_current_deadline_at(d.pop("current_deadline_at"))

        def _parse_current_finished_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                current_finished_at_type_0 = datetime.datetime.fromisoformat(data)

                return current_finished_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        current_finished_at = _parse_current_finished_at(d.pop("current_finished_at"))

        def _parse_current_run_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                current_run_id_type_0 = UUID(data)

                return current_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        current_run_id = _parse_current_run_id(d.pop("current_run_id"))

        def _parse_current_started_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                current_started_at_type_0 = datetime.datetime.fromisoformat(data)

                return current_started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        current_started_at = _parse_current_started_at(d.pop("current_started_at"))

        enabled = d.pop("enabled")

        def _parse_enabled_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                enabled_at_type_0 = datetime.datetime.fromisoformat(data)

                return enabled_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        enabled_at = _parse_enabled_at(d.pop("enabled_at"))

        execution_state = IntegrationExecutionState(d.pop("execution_state"))

        health = IntegrationHealth(d.pop("health"))

        id = UUID(d.pop("id"))

        is_stale = d.pop("is_stale")

        key = d.pop("key")

        def _parse_last_changes_detected(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        last_changes_detected = _parse_last_changes_detected(
            d.pop("last_changes_detected")
        )

        def _parse_last_error_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_error_code = _parse_last_error_code(d.pop("last_error_code"))

        def _parse_last_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_error_message = _parse_last_error_message(d.pop("last_error_message"))

        def _parse_last_finished_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_finished_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_finished_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_finished_at = _parse_last_finished_at(d.pop("last_finished_at"))

        def _parse_last_result(data: object) -> IntegrationResult | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_result_type_0 = IntegrationResult(data)

                return last_result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(IntegrationResult | None, data)

        last_result = _parse_last_result(d.pop("last_result"))

        def _parse_last_success_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_success_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_success_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_success_at = _parse_last_success_at(d.pop("last_success_at"))

        ledger_id = UUID(d.pop("ledger_id"))

        name = d.pop("name")

        provider = d.pop("provider")

        revision = d.pop("revision")

        run_timeout_seconds = d.pop("run_timeout_seconds")

        stale_after_seconds = d.pop("stale_after_seconds")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        integration_public = cls(
            category_ids=category_ids,
            created_at=created_at,
            current_deadline_at=current_deadline_at,
            current_finished_at=current_finished_at,
            current_run_id=current_run_id,
            current_started_at=current_started_at,
            enabled=enabled,
            enabled_at=enabled_at,
            execution_state=execution_state,
            health=health,
            id=id,
            is_stale=is_stale,
            key=key,
            last_changes_detected=last_changes_detected,
            last_error_code=last_error_code,
            last_error_message=last_error_message,
            last_finished_at=last_finished_at,
            last_result=last_result,
            last_success_at=last_success_at,
            ledger_id=ledger_id,
            name=name,
            provider=provider,
            revision=revision,
            run_timeout_seconds=run_timeout_seconds,
            stale_after_seconds=stale_after_seconds,
            updated_at=updated_at,
        )

        integration_public.additional_properties = d
        return integration_public

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
