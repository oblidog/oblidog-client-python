from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.obligation_component_public_metadata_type_0 import (
        ObligationComponentPublicMetadataType0,
    )


T = TypeVar("T", bound="ObligationComponentPublic")


@_attrs_define
class ObligationComponentPublic:
    """
    Attributes:
        amount (None | str):
        created_at (datetime.datetime):
        external_id (None | str):
        id (UUID):
        label (str):
        metadata (None | ObligationComponentPublicMetadataType0):
        obligation_id (UUID):
        source (None | str):
        type_ (str):
        updated_at (datetime.datetime):
    """

    amount: None | str
    created_at: datetime.datetime
    external_id: None | str
    id: UUID
    label: str
    metadata: None | ObligationComponentPublicMetadataType0
    obligation_id: UUID
    source: None | str
    type_: str
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.obligation_component_public_metadata_type_0 import (
            ObligationComponentPublicMetadataType0,
        )

        amount: None | str
        amount = self.amount

        created_at = self.created_at.isoformat()

        external_id: None | str
        external_id = self.external_id

        id = str(self.id)

        label = self.label

        metadata: dict[str, Any] | None
        if isinstance(self.metadata, ObligationComponentPublicMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        obligation_id = str(self.obligation_id)

        source: None | str
        source = self.source

        type_ = self.type_

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "created_at": created_at,
                "external_id": external_id,
                "id": id,
                "label": label,
                "metadata": metadata,
                "obligation_id": obligation_id,
                "source": source,
                "type": type_,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.obligation_component_public_metadata_type_0 import (
            ObligationComponentPublicMetadataType0,
        )

        d = dict(src_dict)

        def _parse_amount(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        amount = _parse_amount(d.pop("amount"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_external_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_id = _parse_external_id(d.pop("external_id"))

        id = UUID(d.pop("id"))

        label = d.pop("label")

        def _parse_metadata(
            data: object,
        ) -> None | ObligationComponentPublicMetadataType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ObligationComponentPublicMetadataType0.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ObligationComponentPublicMetadataType0, data)

        metadata = _parse_metadata(d.pop("metadata"))

        obligation_id = UUID(d.pop("obligation_id"))

        def _parse_source(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        source = _parse_source(d.pop("source"))

        type_ = d.pop("type")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        obligation_component_public = cls(
            amount=amount,
            created_at=created_at,
            external_id=external_id,
            id=id,
            label=label,
            metadata=metadata,
            obligation_id=obligation_id,
            source=source,
            type_=type_,
            updated_at=updated_at,
        )

        obligation_component_public.additional_properties = d
        return obligation_component_public

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
