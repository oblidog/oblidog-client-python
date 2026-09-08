from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar
from uuid import UUID

from attrs import define as _attrs_define

T = TypeVar("T", bound="IntegrationRunStart")


@_attrs_define
class IntegrationRunStart:
    """
    Attributes:
        expected_revision (int):
        run_id (UUID):
    """

    expected_revision: int
    run_id: UUID

    def to_dict(self) -> dict[str, Any]:
        expected_revision = self.expected_revision

        run_id = str(self.run_id)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "expected_revision": expected_revision,
                "run_id": run_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        expected_revision = d.pop("expected_revision")

        run_id = UUID(d.pop("run_id"))

        integration_run_start = cls(
            expected_revision=expected_revision,
            run_id=run_id,
        )

        return integration_run_start
