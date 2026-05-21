# Datamine Studio Filde Converter

This folder contains the Go implementation of the Datamine Studio mining software binary file converter. It is the production version of the tool: fast, portable, dependency‑free, and suitable for integration into mining data science workflows.

A Python version now sits alongside it in `../dmconv-python/`.

A legacy R version stored in the `legacy/` folder and an R with C version stored in the `specification/` folder are included to show the evolution of the tool from R to C to Go.

The tool parse Datamine Studio binary `.dm` files and exports the contents to open, analysis‑friendly formats such as Parquet and CSV.

The converter exists because Datamine Studio uses proprietary binary formats that typically require access to the software to export data. In many mining workflows, access is limited or unavailable, creating friction and dependency on manual exports.

These implementations remove that dependency. They allow direct ingestion of Datamine files into data science workflows, reproducible pipelines, and automated processes.

## Why This Tool Exists

- Datamine Studio mining software is expensive and often inaccessible
- Users must manually export CSVs using the software
- Workflows become slow, brittle, and non‑reproducible
- Direct binary parsing removes friction and dependency

## Go Version

- Fast, portable, dependency‑free
- Distributed as static binaries (Windows, macOS)
- Suitable for CLI workflows and automated pipelines
- Future direction: extract core logic and refactor into an interface‑based library

## R Version

- Original implementation used for early DS workflows
- Useful for reference, validation, and reproducibility
- Demonstrates the evolution from prototype → production
- There is a C read and write function to speed up R.

See:
[`legacy/README.md`](legacy/README.md)
[`specification/README.md`](specification/README.md)

## Features

- Parses Datamine `.dm` binary files directly
- Exports to Parquet and CSV (other formats in future versions)
- No Datamine license required
- Static binaries for Windows and macOS
- Deterministic, reproducible output
- Simple CLI interface

## Structure

```
/dmconv               # Go production implementation (CLI + library)
├── cmd/              # Go commands
├── internal/         # Go datamine package files
├── legacy/           # Original R prototype implementation
└── specification/    # C code for speeding up the R implementation (not used)
```

## Compiling from source

You will need to download and install the Go compiler.

Open a terminal window, change directory into the source folder and the run the Go compiler.

```
go build .
```

## Downloads

Prebuilt binaries are available on the Releases page:

- Windows (amd64)
- MacOS (arm64)

See: https://github.com/nimmo-matthew/mining-ds-toolkit/releases

## Usage

Convert a Datamine file to Parquet:

```
./dmconv input.dm
./dmconv input.dm --csv
```

The open_parquet.qmd Quarto markdown is for testing the output Arrow Parquet file in R.

## Design Notes

- Written in Go for portability and deployment simplicity
- No external dependencies
- Designed for offline use in field or site environments
- Suitable for embedding into larger Go pipelines

## Future Directions

- Extract core logic into a public package
- Add support for additional export file types
- Provide a streaming API for large files
- Add bindings for Python/R if needed

## Repository Context

This implementation is part of the mining‑ds‑toolkit.

It reflects the shift from R prototypes to Go‑based production tools.
