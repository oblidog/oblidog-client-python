from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ObligationNoteAppend")


@_attrs_define
class ObligationNoteAppend:
    """
    Attributes:
        text (str):
    """

    text: str

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        text = d.pop("text")

        obligation_note_append = cls(
            text=text,
        )

        return obligation_note_append
