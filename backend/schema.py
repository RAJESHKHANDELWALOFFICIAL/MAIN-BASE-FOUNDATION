"""MAIN BASE FOUNDATION database schema.

Central schema definitions for the database foundation.

This module contains only database schema creation.
Business logic belongs in the appropriate service/controller modules.
"""

from __future__ import annotations

from .service import DatabaseService


class DatabaseSchema:
    """Create and maintain core database tables."""

    def __init__(
        self,
        database_service: DatabaseService | None = None,
    ) -> None:
        self.service = (
            database_service
            or DatabaseService()
        )

    def create_core_tables(self) -> dict:
        """Create the core foundation tables."""

        self.service.initialize()

        self.service.execute(
            """
            CREATE TABLE IF NOT EXISTS system_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        return {
            "success": True,
            "status": "CORE_SCHEMA_READY",
        }

    def status(self) -> dict:
        """Return schema status."""

        return {
            "schema": "DatabaseSchema",
            "status": "READY",
        }


__all__ = [
    "DatabaseSchema",
]
