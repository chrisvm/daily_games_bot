from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence
from colorama import init as colorama_init, Fore, Style

from daily_games_bot.parsing.chat import ChatTranscriptParser


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
    colorama_init()

    args = parse_arguments()
    print(args)

    match args.command:
        case "ingest":
            path = args.path.expanduser()
            if not path.is_file():
                print(
                    f"🛑 {Fore.RED}file '{Fore.CYAN}{path}{Fore.RED}' not found or not a file{Style.RESET_ALL}"
                )
                sys.exit(1)

            with open(path, encoding="utf-8") as f:
                raw_lines = f.read()

            print(
                f"{Fore.GREEN}ingesting results from {Fore.CYAN}{path}{Style.RESET_ALL}"
            )
            messages = ChatTranscriptParser.parse(raw_lines)
            print(
                f"{Fore.GREEN}parsed {Fore.CYAN}{len(messages)}{Fore.GREEN} messages{Style.RESET_ALL}"
            )
        case _:
            print(
                f"{Fore.YELLOW}command '{Fore.CYAN}{args.command}' not found{Style.RESET_ALL}"
            )


if __name__ == "__main__":
    main()
