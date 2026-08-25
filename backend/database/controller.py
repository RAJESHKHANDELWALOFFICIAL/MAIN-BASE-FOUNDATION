"""MAIN BASE FOUNDATION database controller.

Controller layer for database operations.

This module keeps higher-level backend code independent from the
internal DatabaseService implementation.
"""

from __future__ import annotations

from typing import Any, Iterable, Optional, Sequence

from .service import DatabaseService


class DatabaseController:
    """Controller facade for the MAIN BASE FOUNDATION database layer."""

    def __init__(
        self,
        database_service: Optional[DatabaseService] = None,
    ) -> None:
        self.service = (
            database_service
            or DatabaseService()
        )

    # ------------------------------------------------------------------
    # LIFECYCLE
    # ------------------------------------------------------------------

    def connect(self) -> dict:
        """Connect to the database."""

        return self.service.connect()

    def disconnect(self) -> dict:
        """Disconnect from the database."""

        return self.service.disconnect()

    def initialize(self) -> dict:
        """Initialize the database foundation."""

        return self.service.initialize()

    # ------------------------------------------------------------------
    # EXECUTION
    # ------------------------------------------------------------------

    def execute(
        self,
        query: str,
        parameters: Sequence[Any] | Iterable[Any] = (),
    ) -> int:
        """Execute a SQL statement."""

        return self.service.execute(
            query=query,
            parameters=parameters,
        )

    def executemany(
        self,
        query: str,
        parameters: Iterable[Sequence[Any]],
    ) -> int:
        """Execute a SQL statement for multiple parameter sets."""

        return self.service.executemany(
            query=query,
            parameters=parameters,
        )

    # ------------------------------------------------------------------
    # QUERIES
    # ------------------------------------------------------------------

    def fetchone(
        self,
        query: str,
        parameters: Sequence[Any] | Iterable[Any] = (),
    ):
        """Return one database row."""

        return self.service.fetchone(
            query=query,
            parameters=parameters,
        )

    def fetchall(
        self,
        query: str,
        parameters: Sequence[Any] | Iterable[Any] = (),
    ):
        """Return all matching database rows."""

        return self.service.fetchall(
            query=query,
            parameters=parameters,
        )

    # ------------------------------------------------------------------
    # TRANSACTIONS
    # ------------------------------------------------------------------

    def begin(self) -> dict:
        """Begin a database transaction."""

        return self.service.begin()

    def commit(self) -> dict:
        """Commit the current database transaction."""

        return self.service.commit()

    def rollback(self) -> dict:
        """Rollback the current database transaction."""

        return self.service.rollback()

    # ------------------------------------------------------------------
    # STATUS
    # ------------------------------------------------------------------

    def health(self) -> dict:
        """Return database health information."""

        return self.service.health()

    def status(self) -> dict:
        """Return database controller status."""

        return {
            "controller": "DatabaseController",
            "service": self.service.status(),
        }


__all__ = [
    "DatabaseController",
]
