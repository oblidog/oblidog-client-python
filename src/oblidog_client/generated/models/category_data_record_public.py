from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.category_data_record_public_data import CategoryDataRecordPublicData


T = TypeVar("T", bound="CategoryDataRecordPublic")


@_attrs_define
class CategoryDataRecordPublic:
    """
    Attributes:
        created_at (datetime.datetime):
        data (CategoryDataRecordPublicData):
        external_id (None | str):
        id (UUID):
        observed_at (datetime.datetime):
        schema_version (int):
        source (None | str):
    """

    created_at: datetime.datetime
    data: CategoryDataRecordPublicData
    external_id: None | str
    id: UUID
    observed_at: datetime.datetime
    schema_version: int
    source: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        data = self.data.to_dict()

        external_id: None | str
        external_id = self.external_id

        id = str(self.id)

        observed_at = self.observed_at.isoformat()

        schema_version = self.schema_version

        source: None | str
        source = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "data": data,
                "external_id": external_id,
                "id": id,
                "observed_at": observed_at,
                "schema_version": schema_version,
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.category_data_record_public_data import (
            CategoryDataRecordPublicData,
        )

        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        data = CategoryDataRecordPublicData.from_dict(d.pop("data"))

        def _parse_external_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_id = _parse_external_id(d.pop("external_id"))

        id = UUID(d.pop("id"))

        observed_at = datetime.datetime.fromisoformat(d.pop("observed_at"))

        schema_version = d.pop("schema_version")

        def _parse_source(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        source = _parse_source(d.pop("source"))

        category_data_record_public = cls(
            created_at=created_at,
            data=data,
            external_id=external_id,
            id=id,
            observed_at=observed_at,
            schema_version=schema_version,
            source=source,
        )

        category_data_record_public.additional_properties = d
        return category_data_record_public

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
