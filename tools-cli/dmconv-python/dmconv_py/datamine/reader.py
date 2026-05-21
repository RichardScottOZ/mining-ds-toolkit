from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .helpers import number_from_bytes, string_from_bytes
from .types import Data


@dataclass(slots=True)
class Metadata:
    field_name: str
    field_type: str
    logical_rec_pos: int
    word_number: int
    unit: int
    default: object
    size: int


class Reader:
    def __init__(self, content: bytes, byte_size: int) -> None:
        self.content = content
        self.byte_size = byte_size
        self.offset = 0

    def read(self, size: int) -> bytes:
        chunk = self.content[self.offset : self.offset + size]
        if len(chunk) != size:
            raise ValueError("unexpected end of file")
        self.offset += size
        return chunk

    def skip_to_page_boundary(self) -> None:
        page_size = 2048 * self.byte_size
        remainder = self.offset % page_size
        if remainder:
            self.offset += page_size - remainder


def read_dm(filename: str | Path) -> Data:
    path = Path(filename)
    content = path.read_bytes()
    if len(content) < 200:
        raise ValueError("input file is too small")

    byte_size = 1
    if number_from_bytes(content[24 * 8 : 24 * 8 + 8]) == 456789.0:
        byte_size = 2

    reader = Reader(content, byte_size)

    name = reader.read(byte_size * 8)
    directory = reader.read(byte_size * 8)
    description = reader.read(byte_size * 64)
    reader.read(byte_size * 8)  # owner
    reader.read(byte_size * 4)  # owner perms
    reader.read(byte_size * 4)  # other perms
    modify_date = reader.read(byte_size * 4)
    num_fields = reader.read(byte_size * 4)
    num_pages = reader.read(byte_size * 4)
    recs_last_page = reader.read(byte_size * 4)

    print(string_from_bytes(name, byte_size), string_from_bytes(directory, byte_size))
    print(string_from_bytes(description, byte_size))

    modify_value = number_from_bytes(modify_date)
    print(f"Modify date: {modify_value:g}")
    if modify_value < 720101 or modify_value > 99991231:
        print("Byte swapped")

    field_count = int(number_from_bytes(num_fields))
    if field_count <= 0 or field_count > 64:
        raise ValueError("invalid file")

    page_count = int(number_from_bytes(num_pages))
    records_last_page = int(number_from_bytes(recs_last_page))

    metadata = _read_metadata(reader, field_count, byte_size)
    for item in metadata:
        print(
            "{Field: %s, Type: %s, Size: %d, Default: %s, Implicit: %d}"
            % (
                item.field_name,
                item.field_type,
                item.size,
                item.default,
                item.logical_rec_pos,
            )
        )

    reader.skip_to_page_boundary()

    implicit_count = sum(1 for item in metadata if item.logical_rec_pos > 0)
    records_per_page = 508 // implicit_count if implicit_count else 0
    row_count = (page_count - 2) * records_per_page + records_last_page
    print(f"Number of rows: {row_count}")

    names = [item.field_name for item in metadata]
    types = [item.field_type for item in metadata]
    columns: list[list[object]] = [[None] * row_count for _ in metadata]

    remaining_pages = max(page_count - 1, 0)
    row_index = 0
    for page_index in range(remaining_pages):
        page_rows = records_last_page if page_index + 1 == remaining_pages else records_per_page
        for _ in range(page_rows):
            for column_index, item in enumerate(metadata):
                if item.logical_rec_pos == 0:
                    columns[column_index][row_index] = item.default
                    continue

                value_bytes = reader.read(item.size)
                if item.field_type == "N":
                    columns[column_index][row_index] = number_from_bytes(value_bytes)
                else:
                    columns[column_index][row_index] = string_from_bytes(value_bytes, byte_size)
            row_index += 1
        reader.skip_to_page_boundary()

    return Data(names=names, types=types, data=columns)


def _read_metadata(reader: Reader, field_count: int, byte_size: int) -> list[Metadata]:
    result: list[Metadata] = []
    previous_name = ""

    for _ in range(field_count):
        field_name = string_from_bytes(reader.read(byte_size * 8), byte_size)
        field_type = reader.read(byte_size * 4)[:1].decode("latin1")
        logical_rec_pos = int(number_from_bytes(reader.read(byte_size * 4)))
        word_number = int(number_from_bytes(reader.read(byte_size * 4)))
        unit = int(number_from_bytes(reader.read(byte_size * 4)))

        if field_type == "N":
            default: object = number_from_bytes(reader.read(byte_size * 4))
        else:
            default = string_from_bytes(reader.read(byte_size * 4), byte_size)

        item = Metadata(
            field_name=field_name,
            field_type=field_type,
            logical_rec_pos=logical_rec_pos,
            word_number=word_number,
            unit=unit,
            default=default,
            size=4 * byte_size,
        )

        if previous_name == item.field_name and result:
            result[-1].size += 4 * byte_size
            result[-1].default = f"{result[-1].default}{item.default}"
        else:
            result.append(item)
            previous_name = item.field_name

    return result
