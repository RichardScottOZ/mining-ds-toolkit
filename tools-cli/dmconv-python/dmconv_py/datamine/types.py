from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Data:
    names: list[str]
    types: list[str]
    data: list[list[object]]
