from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_obligation_component_upsert_metadata_type_0 import (
        IntegrationObligationComponentUpsertMetadataType0,
    )


T = TypeVar("T", bound="IntegrationObligationComponentUpsert")


@_attrs_define
class IntegrationObligationComponentUpsert:
    """An obligation component identified within its authenticated integration.

    Attributes:
        external_id (str):
        label (str):
        type_ (str):
        amount (float | None | str | Unset):
        metadata (IntegrationObligationComponentUpsertMetadataType0 | None | Unset):
    """

    external_id: str
    label: str
    type_: str
    amount: float | None | str | Unset = UNSET
    metadata: IntegrationObligationComponentUpsertMetadataType0 | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.integration_obligation_component_upsert_metadata_type_0 import (
            IntegrationObligationComponentUpsertMetadataType0,
        )

        external_id = self.external_id

        label = self.label

        type_ = self.type_

        amount: float | None | str | Unset
        if isinstance(self.amount, Unset):
            amount = UNSET
        else:
            amount = self.amount

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(
            self.metadata, IntegrationObligationComponentUpsertMetadataType0
        ):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "external_id": external_id,
                "label": label,
                "type": type_,
            }
        )
        if amount is not UNSET:
            field_dict["amount"] = amount
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.integration_obligation_component_upsert_metadata_type_0 import (
            IntegrationObligationComponentUpsertMetadataType0,
        )

        d = dict(src_dict)
        external_id = d.pop("external_id")

        label = d.pop("label")

        type_ = d.pop("type")

        def _parse_amount(data: object) -> float | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | str | Unset, data)

        amount = _parse_amount(d.pop("amount", UNSET))

        def _parse_metadata(
            data: object,
        ) -> IntegrationObligationComponentUpsertMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = (
                    IntegrationObligationComponentUpsertMetadataType0.from_dict(data)
                )

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                IntegrationObligationComponentUpsertMetadataType0 | None | Unset, data
            )

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        integration_obligation_component_upsert = cls(
            external_id=external_id,
            label=label,
            type_=type_,
            amount=amount,
            metadata=metadata,
        )

        return integration_obligation_component_upsert
