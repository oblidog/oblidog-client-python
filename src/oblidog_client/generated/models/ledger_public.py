from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LedgerPublic")


@_attrs_define
class LedgerPublic:
    """
    Attributes:
        created_at (datetime.datetime):
        description (None | str):
        id (UUID):
        name (str):
        owner_user_id (UUID):
        updated_at (datetime.datetime):
    """

    created_at: datetime.datetime
    description: None | str
    id: UUID
    name: str
    owner_user_id: UUID
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        description: None | str
        description = self.description

        id = str(self.id)

        name = self.name

        owner_user_id = str(self.owner_user_id)

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "description": description,
                "id": id,
                "name": name,
                "owner_user_id": owner_user_id,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        id = UUID(d.pop("id"))

        name = d.pop("name")

        owner_user_id = UUID(d.pop("owner_user_id"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        ledger_public = cls(
            created_at=created_at,
            description=description,
            id=id,
            name=name,
            owner_user_id=owner_user_id,
            updated_at=updated_at,
        )

        ledger_public.additional_properties = d
        return ledger_public

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
