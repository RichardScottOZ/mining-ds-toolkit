from __future__ import annotations

import struct


def number_from_bytes(raw: bytes) -> float:
    if len(raw) == 4:
        return float(struct.unpack("<f", raw)[0])
    return float(struct.unpack("<d", raw)[0])


def string_from_bytes(raw: bytes, byte_size: int) -> str:
    if byte_size == 1:
        return raw.decode("latin1").strip()

    compact = bytearray()
    for offset in range(0, len(raw), 8):
        compact.extend(raw[offset : offset + 4])
    return bytes(compact).decode("latin1").strip()
