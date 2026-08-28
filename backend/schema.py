"""MAIN BASE FOUNDATION database schema.

Central schema definitions for the database foundation.

This module is responsible for creating and validating the core
database schema. Business logic belongs in higher-level modules.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .service import DatabaseService


class DatabaseSchema:
    """Manage the core database schema."""

    CORE_TABLES = (
        "system_metadata",
    )

    def __init__(
        self,
        database_service: DatabaseService | None = None,
    ) -> None:
        self.service = (
            database_service
            or DatabaseService()
        )

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    def create_core_tables(self) -> dict:
        """Create all core database tables."""

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
            "tables": list(self.CORE_TABLES),
        }

    # ------------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------------

    def validate(self) -> dict:
        """Validate that all required core tables exist."""

        rows = self.service.fetchall(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        )

        existing = {
            row["name"]
            for row in rows
        }

        missing = [
            table
            for table in self.CORE_TABLES
            if table not in existing
        ]

        return {
            "success": len(missing) == 0,
            "status": (
                "VALID"
                if not missing
                else "INVALID"
            ),
            "required_tables": list(
                self.CORE_TABLES
            ),
            "existing_tables": sorted(
                existing
            ),
            "missing_tables": missing,
        }

    # ------------------------------------------------------------------
    # TABLES
    # ------------------------------------------------------------------

    def tables(self) -> List[str]:
        """Return the names of all database tables."""

        rows = self.service.fetchall(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        )

        return [
            row["name"]
            for row in rows
        ]

    # ------------------------------------------------------------------
    # STATUS
    # ------------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        """Return schema status."""

        validation = self.validate()

        return {
            "schema": "DatabaseSchema",
            "status": validation["status"],
            "required_tables": validation[
                "required_tables"
            ],
            "missing_tables": validation[
                "missing_tables"
            ],
        }


__all__ = [
    "DatabaseSchema",
]
