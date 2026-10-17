from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.api_error_response_code import ApiErrorResponseCode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_error_response_params import ApiErrorResponseParams


T = TypeVar("T", bound="ApiErrorResponse")


@_attrs_define
class ApiErrorResponse:
    """
    Attributes:
        code (ApiErrorResponseCode):
        detail (Any):
        params (ApiErrorResponseParams | Unset):
    """

    code: ApiErrorResponseCode
    detail: Any
    params: ApiErrorResponseParams | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        detail = self.detail

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
        from ..models.api_error_response_params import ApiErrorResponseParams

        d = dict(src_dict)
        code = ApiErrorResponseCode(d.pop("code"))

        detail = d.pop("detail")

        _params = d.pop("params", UNSET)
        params: ApiErrorResponseParams | Unset
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = ApiErrorResponseParams.from_dict(_params)

        api_error_response = cls(
            code=code,
            detail=detail,
            params=params,
        )

        api_error_response.additional_properties = d
        return api_error_response

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
