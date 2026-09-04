from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.obligation_component_upsert_metadata_type_0 import (
        ObligationComponentUpsertMetadataType0,
    )


T = TypeVar("T", bound="ObligationComponentUpsert")


@_attrs_define
class ObligationComponentUpsert:
    """
    Attributes:
        label (str):
        type_ (str):
        amount (float | None | str | Unset):
        external_id (None | str | Unset):
        metadata (None | ObligationComponentUpsertMetadataType0 | Unset):
        source (None | str | Unset):
    """

    label: str
    type_: str
    amount: float | None | str | Unset = UNSET
    external_id: None | str | Unset = UNSET
    metadata: None | ObligationComponentUpsertMetadataType0 | Unset = UNSET
    source: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.obligation_component_upsert_metadata_type_0 import (
            ObligationComponentUpsertMetadataType0,
        )

        label = self.label

        type_ = self.type_

        amount: float | None | str | Unset
        if isinstance(self.amount, Unset):
            amount = UNSET
        else:
            amount = self.amount

        external_id: None | str | Unset
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, ObligationComponentUpsertMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        source: None | str | Unset
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "label": label,
                "type": type_,
            }
        )
        if amount is not UNSET:
            field_dict["amount"] = amount
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.obligation_component_upsert_metadata_type_0 import (
            ObligationComponentUpsertMetadataType0,
        )

        d = dict(src_dict)
        label = d.pop("label")

        type_ = d.pop("type")

        def _parse_amount(data: object) -> float | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | str | Unset, data)

        amount = _parse_amount(d.pop("amount", UNSET))

        def _parse_external_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_metadata(
            data: object,
        ) -> None | ObligationComponentUpsertMetadataType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ObligationComponentUpsertMetadataType0.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ObligationComponentUpsertMetadataType0 | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_source(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source = _parse_source(d.pop("source", UNSET))

        obligation_component_upsert = cls(
            label=label,
            type_=type_,
            amount=amount,
            external_id=external_id,
            metadata=metadata,
            source=source,
        )

        return obligation_component_upsert
