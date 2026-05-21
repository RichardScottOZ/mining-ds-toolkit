# dmconv-python

Python implementation of the Datamine Studio `.dm` converter, added alongside the existing Go version.

## Features

- reads Datamine Studio binary `.dm` files
- exports to Parquet by default
- exports to CSV with `--csv`
- keeps the same column set and output shape as the Go implementation

## Install

From this folder:

```bash
python -m pip install -e .
```

## Usage

Convert to Parquet:

```bash
dmconv-python out ../dmconv/_geology.dm
```

Convert to CSV:

```bash
dmconv-python out ../dmconv/_geology.dm --csv
```

You can also run it as a module:

```bash
python -m dmconv_py out ../dmconv/_geology.dm --csv
```
