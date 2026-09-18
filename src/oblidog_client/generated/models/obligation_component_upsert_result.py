from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.mutation_result import MutationResult

if TYPE_CHECKING:
    from ..models.obligation_component_public import ObligationComponentPublic


T = TypeVar("T", bound="ObligationComponentUpsertResult")


@_attrs_define
class ObligationComponentUpsertResult:
    """
    Attributes:
        component (ObligationComponentPublic):
        result (MutationResult):
    """

    component: ObligationComponentPublic
    result: MutationResult
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        component = self.component.to_dict()

        result = self.result.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "component": component,
                "result": result,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.obligation_component_public import ObligationComponentPublic

        d = dict(src_dict)
        component = ObligationComponentPublic.from_dict(d.pop("component"))

        result = MutationResult(d.pop("result"))

        obligation_component_upsert_result = cls(
            component=component,
            result=result,
        )

        obligation_component_upsert_result.additional_properties = d
        return obligation_component_upsert_result

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
