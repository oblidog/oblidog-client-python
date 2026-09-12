from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IntegrationContextIntegrationPublic")


@_attrs_define
class IntegrationContextIntegrationPublic:
    """
    Attributes:
        enabled (bool):
        id (UUID):
        name (str):
        revision (int):
    """

    enabled: bool
    id: UUID
    name: str
    revision: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        id = str(self.id)

        name = self.name

        revision = self.revision

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "id": id,
                "name": name,
                "revision": revision,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        id = UUID(d.pop("id"))

        name = d.pop("name")

        revision = d.pop("revision")

        integration_context_integration_public = cls(
            enabled=enabled,
            id=id,
            name=name,
            revision=revision,
        )

        integration_context_integration_public.additional_properties = d
        return integration_context_integration_public

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
