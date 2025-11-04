# Daily Games Bot

Daily Games Bot is a Discord bot scaffold that schedules a daily post in a Discord forum channel and will eventually parse the community's game results to track wins across titles such as Clues by Sam, kindahard.golf, and angle.wtf.

## Project Goals
- Post a thread every day with the current date and a running counter.
- Persist the post counter and other bot settings in a JSON-backed configuration file.
- Parse shared game result blocks and persist structured data with SQLModel.
- Provide utilities for ingesting historical results and surfacing tallies.

## Repository Layout
- `src/daily_games_bot/bot.py` – discord.py bot, daily thread scheduler, and submission hook stubs.
- `src/daily_games_bot/parsing.py` – placeholder parsing entry point for turning pasted text into models.
- `src/daily_games_bot/modeling.py` – SQLModel tables for each supported game.
- `scripts/run_bot.py` – development launcher that will wire up configuration and the Discord token.
- `scripts/data_insert.py` – CLI scaffolding for loading parsed results from files.
- `config.json` – persisted configuration (post counter and other bot settings).

## Getting Started
### Prerequisites
- Python 3.13 or newer.
- A Discord application with a bot token and access to a forum channel.
- (Optional) [uv](https://github.com/astral-sh/uv) if you prefer managing the environment via the provided `uv.lock`.

### Installation
1. Create and activate a virtual environment.
2. Install the project in editable mode:
   ```bash
   pip install -e .
   ```
   Or, with uv:
   ```bash
   uv sync
   ```

## Configuration
- Copy `config.json` if necessary and ensure it contains at least:
  ```json
  {
    "forum_channel_id": 0,
    "current_post_number": 1
  }
  ```
- The supplied placeholder file tracks the counter under `post_count`; update it to `current_post_number` once `ConfigManager` is implemented.
- Extend the JSON payload as needed when you add more runtime settings (timezones, guild IDs, etc.).
- Persisting updates is handled by `ConfigManager`, which still needs its load/persist logic filled in.

Store your Discord bot token securely (environment variable, secret manager, etc.). The launcher is expected to read it when the wiring work lands.

## Running the Bot (once wiring is complete)
1. Export the bot token, for example:
   ```bash
   export DISCORD_BOT_TOKEN=your-token-here
   ```
2. Execute the launcher:
   ```bash
   python scripts/run_bot.py
   ```
3. The `DailyGamesBot` task loop will attempt to post a new thread every day at noon UTC. Adjust the schedule in `DailyGamesBot.post_scheduler` when you add richer scheduling support.

## Development Notes
- **Parsing:** `ResultsParsing.parse` currently returns `None`; implement game-specific logic to return the SQLModel defined for each game type.
- **Storage:** `modeling.py` defines tables for multiple games. You can use SQLModel's session system to persist parsed submissions to any supported database engine.
- **Commands & Events:** The bot class wires `process_submission`, which is the hook for responding to new messages in the thread. Flesh this out to call your parsers and update tallies.
- **Scripts:** `scripts/data_insert.py` provides a CLI skeleton (`ingest` subcommand) for bulk-loading results. Add actual ingestion logic once parsers and storage are in place.
- **Logging:** `scripts/run_bot.py` configures standard logging; expand with structured logs or Discord webhooks as needed.

## Roadmap Ideas
- Finish `ConfigManager` to load/save JSON and expose convenience helpers.
- Implement per-game parsing and validation, including error reporting in Discord.
- Persist player tallies and surface summaries in the thread after each submission.
- Add administrative commands for resetting counters, backfilling results, or generating leaderboards.
- Write automated tests for parsing logic and configuration management.
