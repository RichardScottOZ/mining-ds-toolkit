from __future__ import annotations

from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from .types import Data


def write_parquet(data: Data, filename: str | Path) -> None:
    path = Path(filename)
    schema_fields = []
    table_data: dict[str, list[object]] = {}

    for name, value_type, column in zip(data.names, data.types, data.data, strict=True):
        if value_type == "N":
            schema_fields.append(pa.field(name, pa.float64()))
            table_data[name] = [float(value) for value in column]
        else:
            schema_fields.append(pa.field(name, pa.string()))
            table_data[name] = [str(value) for value in column]

    table = pa.Table.from_pydict(table_data, schema=pa.schema(schema_fields))
    pq.write_table(table, path)
