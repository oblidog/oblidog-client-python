from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.integration_conflict_response_code import IntegrationConflictResponseCode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_conflict_detail import IntegrationConflictDetail
    from ..models.integration_conflict_response_params import (
        IntegrationConflictResponseParams,
    )


T = TypeVar("T", bound="IntegrationConflictResponse")


@_attrs_define
class IntegrationConflictResponse:
    """
    Attributes:
        code (IntegrationConflictResponseCode):
        detail (IntegrationConflictDetail):
        params (IntegrationConflictResponseParams | Unset):
    """

    code: IntegrationConflictResponseCode
    detail: IntegrationConflictDetail
    params: IntegrationConflictResponseParams | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        detail = self.detail.to_dict()

        params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "detail": detail,
            }
        )
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.integration_conflict_detail import IntegrationConflictDetail
        from ..models.integration_conflict_response_params import (
            IntegrationConflictResponseParams,
        )

        d = dict(src_dict)
        code = IntegrationConflictResponseCode(d.pop("code"))

        detail = IntegrationConflictDetail.from_dict(d.pop("detail"))

        _params = d.pop("params", UNSET)
        params: IntegrationConflictResponseParams | Unset
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = IntegrationConflictResponseParams.from_dict(_params)

        integration_conflict_response = cls(
            code=code,
            detail=detail,
            params=params,
        )

        integration_conflict_response.additional_properties = d
        return integration_conflict_response

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
