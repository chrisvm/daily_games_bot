"""Data models for parsed game results."""

from __future__ import annotations

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class FramedResult(SQLModel, table=True):
    """Parsed results for Framed daily game submissions."""

    id: str = Field(primary_key=True, index=True)
    answers_count: int
    failed: bool


class AngleWtfResult(SQLModel, table=True):
    """Parsed results for angle.wtf daily game submissions."""

    id: str = Field(primary_key=True, index=True)
    failed: bool
    guesses: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    off_by: int


class CluesBySamResult(SQLModel, table=True):
    """Parsed results for Clues by Sam daily game submissions."""

    id: str = Field(primary_key=True, index=True)
    time_in_seconds: int
    solution: list[list[str]] = Field(default_factory=list, sa_column=Column(JSON))


class KindahardGolfResult(SQLModel, table=True):
    """Parsed results for kindahard.golf daily game submissions."""

    id: str = Field(primary_key=True, index=True)
    hit_count: int
    holes: list[int] = Field(default_factory=list, sa_column=Column(JSON))


class CostcodleResult(SQLModel, table=True):
    """Parsed results for Costco-dle daily game submissions."""

    id: str = Field(primary_key=True, index=True)
    answers: list[tuple[str, str]] = Field(default_factory=list, sa_column=Column(JSON))
