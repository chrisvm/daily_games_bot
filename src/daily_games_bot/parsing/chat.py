from __future__ import annotations

from datetime import datetime
from typing import Iterable

from pydantic import BaseModel, ConfigDict
from pyparsing import (
    Literal,
    Optional,
    ParseBaseException,
    ParserElement,
    Regex,
    Suppress,
    White,
    oneOf,
    restOfLine,
)


class ChatMessage(BaseModel):
    """Single message entry from an exported chat transcript."""

    model_config = ConfigDict(frozen=True)

    timestamp: datetime
    author: str
    content: str

    def lines(self) -> list[str]:
        """Return the message content split into individual lines."""
        return self.content.splitlines()


class ChatTranscriptParser:
    """Parser for WhatsApp-style chat transcripts exported to plain text."""

    _DATETIME_FORMATS = ("%m/%d/%y %I:%M:%S %p", "%m/%d/%y %I:%M %p")
    ParserElement.enable_packrat()
    _HEADER = (
        Suppress("[")
        + Regex(r"\d{1,2}/\d{1,2}/\d{2}")("date")
        + Suppress(",")
        + Regex(r"\d{1,2}:\d{2}(?::\d{2})?")("time")
        + Optional(Literal("\u202f")).suppress()
        + Optional(White(" ")).suppress()
        + oneOf("AM PM")("ampm")
        + Suppress("]")
        + Optional(White(" \t")).suppress()
        + Regex(r"[^:]+")("author")
        + Suppress(":")
        + Optional(White(" ")).suppress()
        + Optional(restOfLine, default="")("body")
    )

    @classmethod
    def parse(cls, raw: str) -> list[ChatMessage]:
        """Parse the raw transcript into individual messages."""
        if not raw:
            return []

        messages: list[ChatMessage] = []
        current_header: dict[str, str] | None = None
        body_lines: list[str] = []

        for line in cls._iter_lines(raw):
            try:
                parsed = cls._HEADER.parse_string(line, parse_all=True)
            except ParseBaseException:
                parsed = None

            if parsed:
                if current_header is not None:
                    messages.append(cls._build_message(current_header, body_lines))
                current_header = parsed.as_dict()
                starting_body = current_header.pop("body", "")
                body_lines = [starting_body] if starting_body else []
            else:
                if current_header is None:
                    continue
                body_lines.append(line)

        if current_header is not None:
            messages.append(cls._build_message(current_header, body_lines))

        return messages

    @classmethod
    def _build_message(
        cls, header: dict[str, str], body_lines: Iterable[str]
    ) -> ChatMessage:
        timestamp = cls._parse_timestamp(header["date"], header["time"], header["ampm"])
        content = "\n".join(body_lines).rstrip("\n")
        author = header["author"].strip()
        return ChatMessage(timestamp=timestamp, author=author, content=content)

    @staticmethod
    def _iter_lines(raw: str) -> Iterable[str]:
        for line in raw.splitlines():
            yield line.replace("\u202f", " ").rstrip("\r")

    @classmethod
    def _parse_timestamp(cls, date: str, time: str, ampm: str) -> datetime:
        date_time = f"{date} {time} {ampm}".replace("\u202f", " ")
        for fmt in cls._DATETIME_FORMATS:
            try:
                return datetime.strptime(date_time, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse date/time '{date_time}'")
