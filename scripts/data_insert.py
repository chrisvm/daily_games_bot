from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Configure CLI arguments for data ingestion helpers."""
    parser = argparse.ArgumentParser(
        description="Utilities for loading daily game results into storage."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser(
        "ingest", help="Ingest parsed game results from a file."
    )
    ingest_parser.add_argument(
        "path",
        type=Path,
        help="Path to a file containing game result submissions.",
    )

    return parser.parse_args(argv)


def main():
    args = parse_arguments(sys.argv)
    print(args)


if __name__ == "__main__":
    main()
