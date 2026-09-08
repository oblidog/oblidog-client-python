from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define

from ..models.integration_result import IntegrationResult

if TYPE_CHECKING:
    from ..models.integration_run_error import IntegrationRunError


T = TypeVar("T", bound="IntegrationRunFinish")


@_attrs_define
class IntegrationRunFinish:
    """
    Attributes:
        changes_detected (bool | None):
        error (IntegrationRunError | None):
        result (IntegrationResult):
        run_id (UUID):
    """

    changes_detected: bool | None
    error: IntegrationRunError | None
    result: IntegrationResult
    run_id: UUID

    def to_dict(self) -> dict[str, Any]:
        from ..models.integration_run_error import IntegrationRunError

        changes_detected: bool | None
        changes_detected = self.changes_detected

        error: dict[str, Any] | None
        if isinstance(self.error, IntegrationRunError):
            error = self.error.to_dict()
        else:
            error = self.error

        result = self.result.value

        run_id = str(self.run_id)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "changes_detected": changes_detected,
                "error": error,
                "result": result,
                "run_id": run_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.integration_run_error import IntegrationRunError

        d = dict(src_dict)

        def _parse_changes_detected(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        changes_detected = _parse_changes_detected(d.pop("changes_detected"))

        def _parse_error(data: object) -> IntegrationRunError | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = IntegrationRunError.from_dict(data)

                return error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(IntegrationRunError | None, data)

        error = _parse_error(d.pop("error"))

        result = IntegrationResult(d.pop("result"))

        run_id = UUID(d.pop("run_id"))

        integration_run_finish = cls(
            changes_detected=changes_detected,
            error=error,
            result=result,
            run_id=run_id,
        )

        return integration_run_finish
