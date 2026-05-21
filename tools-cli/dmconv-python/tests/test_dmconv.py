from __future__ import annotations

import csv
import struct
import tempfile
import unittest
from pathlib import Path

import pyarrow.parquet as pq

from dmconv_py.cli import main
from dmconv_py.datamine import read_dm, write_csv, write_parquet
from dmconv_py.datamine.helpers import number_from_bytes, string_from_bytes


REPO_ROOT = Path(__file__).resolve().parents[3]
GO_SAMPLE = REPO_ROOT / "tools-cli" / "dmconv" / "_geology.dm"


class HelpersTest(unittest.TestCase):
    def test_number_from_float32_bytes(self) -> None:
        self.assertEqual(number_from_bytes(struct.pack("<f", 200.03125)), 200.03125)

    def test_number_from_float64_bytes(self) -> None:
        self.assertEqual(number_from_bytes(struct.pack("<d", 456789.0)), 456789.0)

    def test_string_from_32bit_bytes(self) -> None:
        self.assertEqual(string_from_bytes(b"TEST    ", 1), "TEST")

    def test_string_from_64bit_bytes(self) -> None:
        raw = b"ABCD\x00\x00\x00\x00EFGH\x00\x00\x00\x00"
        self.assertEqual(string_from_bytes(raw, 2), "ABCDEFGH")


class ReaderTest(unittest.TestCase):
    def test_read_dm_sample(self) -> None:
        data = read_dm(GO_SAMPLE)

        self.assertEqual(data.names, ["BHID", "FROM", "TO", "ROCK"])
        self.assertEqual(data.types, ["A", "N", "N", "N"])
        self.assertEqual(len(data.data[0]), 53)
        self.assertEqual(data.data[0][0], "DH2675")
        self.assertEqual(data.data[1][0], 82.0)
        self.assertEqual(data.data[2][0], 100.0)
        self.assertEqual(data.data[3][0], 6.0)


class WriterTest(unittest.TestCase):
    def test_write_csv(self) -> None:
        data = read_dm(GO_SAMPLE)
        with tempfile.TemporaryDirectory() as tempdir:
            output = Path(tempdir) / "sample.csv"
            write_csv(data, output)

            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.reader(handle))

        self.assertEqual(rows[0], ["BHID", "FROM", "TO", "ROCK"])
        self.assertEqual(rows[1], ["DH2675", "82", "100", "6"])
        self.assertEqual(len(rows), 54)

    def test_write_parquet(self) -> None:
        data = read_dm(GO_SAMPLE)
        with tempfile.TemporaryDirectory() as tempdir:
            output = Path(tempdir) / "sample.parquet"
            write_parquet(data, output)
            table = pq.read_table(output)

        self.assertEqual(table.column_names, ["BHID", "FROM", "TO", "ROCK"])
        self.assertEqual(table.num_rows, 53)
        self.assertEqual(table.schema.field("BHID").type.__class__.__name__, "DataType")
        self.assertEqual(table["BHID"][0].as_py(), "DH2675")


class CliTest(unittest.TestCase):
    def test_cli_out_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            source = Path(tempdir) / GO_SAMPLE.name
            source.write_bytes(GO_SAMPLE.read_bytes())

            exit_code = main(["out", str(source), "--csv"])

            self.assertEqual(exit_code, 0)
            self.assertTrue(source.with_suffix(".csv").exists())


if __name__ == "__main__":
    unittest.main()
