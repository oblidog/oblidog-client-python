from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CounterpartySummaryPublic")


@_attrs_define
class CounterpartySummaryPublic:
    """
    Attributes:
        id (UUID):
        logo_url (None | str):
        name (str):
        short_name (None | str):
    """

    id: UUID
    logo_url: None | str
    name: str
    short_name: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        logo_url: None | str
        logo_url = self.logo_url

        name = self.name

        short_name: None | str
        short_name = self.short_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "logo_url": logo_url,
                "name": name,
                "short_name": short_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        def _parse_logo_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        logo_url = _parse_logo_url(d.pop("logo_url"))

        name = d.pop("name")

        def _parse_short_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        short_name = _parse_short_name(d.pop("short_name"))

        counterparty_summary_public = cls(
            id=id,
            logo_url=logo_url,
            name=name,
            short_name=short_name,
        )

        counterparty_summary_public.additional_properties = d
        return counterparty_summary_public

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
