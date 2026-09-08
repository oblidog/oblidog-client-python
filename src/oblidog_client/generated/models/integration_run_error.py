from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="IntegrationRunError")


@_attrs_define
class IntegrationRunError:
    """
    Attributes:
        code (str):
        message (str): Sanitized summary only; never credentials, raw responses or tracebacks.
    """

    code: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        integration_run_error = cls(
            code=code,
            message=message,
        )

        return integration_run_error
