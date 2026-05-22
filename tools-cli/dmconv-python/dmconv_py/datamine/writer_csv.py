from __future__ import annotations

import csv
from pathlib import Path

from .types import Data


def write_csv(data: Data, filename: str | Path) -> None:
    path = Path(filename)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(data.names)
        for row in zip(*data.data, strict=True):
            writer.writerow([_format_csv_value(value) for value in row])


def _format_csv_value(value: object) -> str:
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return repr(value)
    return str(value)
