from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.category_data_record_create_data import CategoryDataRecordCreateData


T = TypeVar("T", bound="CategoryDataRecordCreate")


@_attrs_define
class CategoryDataRecordCreate:
    """
    Attributes:
        data (CategoryDataRecordCreateData):
        observed_at (datetime.datetime):
        external_id (None | str | Unset):
        source (None | str | Unset):
    """

    data: CategoryDataRecordCreateData
    observed_at: datetime.datetime
    external_id: None | str | Unset = UNSET
    source: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        observed_at = self.observed_at.isoformat()

        external_id: None | str | Unset
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        source: None | str | Unset
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
                "observed_at": observed_at,
            }
        )
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.category_data_record_create_data import (
            CategoryDataRecordCreateData,
        )

        d = dict(src_dict)
        data = CategoryDataRecordCreateData.from_dict(d.pop("data"))

        observed_at = datetime.datetime.fromisoformat(d.pop("observed_at"))

        def _parse_external_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_source(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source = _parse_source(d.pop("source", UNSET))

        category_data_record_create = cls(
            data=data,
            observed_at=observed_at,
            external_id=external_id,
            source=source,
        )

        return category_data_record_create
