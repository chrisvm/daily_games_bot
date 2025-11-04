#!/usr/bin/env python3
"""Development launcher for the Daily Games Discord bot."""

from __future__ import annotations

import asyncio
import logging

from daily_games_bot.bot import DailyGamesBot  # noqa F401


async def main() -> None:
    """Entrypoint placeholder until configuration wiring is implemented."""
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=logging.INFO,
    )

    raise NotImplementedError(
        "Wire up ConfigManager and token handling before launching the bot."
    )


if __name__ == "__main__":
    asyncio.run(main())
