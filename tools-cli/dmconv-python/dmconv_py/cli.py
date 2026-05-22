from __future__ import annotations

import argparse
from pathlib import Path

from .datamine import read_dm, write_csv, write_parquet

VERSION = "2026.5"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dmconv-python",
        description="File conversion utility for Datamine files.",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    out_parser = subparsers.add_parser(
        "out",
        help="Export a Datamine binary file to Parquet",
        description=(
            "Converts Datamine Studio binary .dm files into open, "
            "analysis-ready formats."
        ),
    )
    out_parser.add_argument("filename", help="Path to the input .dm file")
    out_parser.add_argument("--csv", action="store_true", help="Write CSV instead of Parquet")
    out_parser.set_defaults(func=run_out)

    about_parser = subparsers.add_parser("about", help="Show information about the tool")
    about_parser.set_defaults(func=run_about)

    return parser


def run_out(args: argparse.Namespace) -> int:
    source = Path(args.filename)
    data = read_dm(source)
    print("Data read successfully!")

    if args.csv:
        output = source.with_suffix(".csv")
        write_csv(data, output)
    else:
        output = source.with_suffix(".parquet")
        write_parquet(data, output)

    print(f"Written to {output}")
    return 0


def run_about(_: argparse.Namespace) -> int:
    print("Datamine Studio file conversion utility.")
    print("Converts .dm files to Parquet or CSV without Datamine Studio.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
