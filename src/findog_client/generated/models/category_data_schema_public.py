from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.category_data_schema_public_schema import (
        CategoryDataSchemaPublicSchema,
    )


T = TypeVar("T", bound="CategoryDataSchemaPublic")


@_attrs_define
class CategoryDataSchemaPublic:
    """
    Attributes:
        created_at (datetime.datetime):
        is_active (bool):
        schema (CategoryDataSchemaPublicSchema):
        version (int):
    """

    created_at: datetime.datetime
    is_active: bool
    schema: CategoryDataSchemaPublicSchema
    version: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        is_active = self.is_active

        schema = self.schema.to_dict()

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "is_active": is_active,
                "schema": schema,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.category_data_schema_public_schema import (
            CategoryDataSchemaPublicSchema,
        )

        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        is_active = d.pop("is_active")

        schema = CategoryDataSchemaPublicSchema.from_dict(d.pop("schema"))

        version = d.pop("version")

        category_data_schema_public = cls(
            created_at=created_at,
            is_active=is_active,
            schema=schema,
            version=version,
        )

        category_data_schema_public.additional_properties = d
        return category_data_schema_public

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
