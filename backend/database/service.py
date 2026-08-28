"""MAIN BASE FOUNDATION database service.

Central database service used by backend modules.

Responsibilities:
- database initialization
- connection lifecycle
- SQL execution
- single-row queries
- multi-row queries
- transactions
- rollback
- health information

The service intentionally keeps the database layer independent from
authentication, authorization, permissions, roles, organizations,
businesses, storage, and other higher-level modules.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from threading import RLock
from typing import Any, Iterable, Optional, Sequence


class DatabaseService:
    """Central database service for MAIN BASE FOUNDATION."""

    def __init__(
        self,
        database_path: Optional[str] = None,
    ) -> None:
        self.database_path = (
            database_path
            or "main_base_foundation.db"
        )

        self._connection: Optional[sqlite3.Connection] = None
        self._lock = RLock()

    # ------------------------------------------------------------------
    # CONNECTION
    # ------------------------------------------------------------------

    def connect(self) -> dict:
        """Open the database connection."""

        with self._lock:
            if self._connection is not None:
                return {
                    "success": True,
                    "status": "ALREADY_CONNECTED",
                    "database": self.database_path,
                }

            path = Path(self.database_path)

            if path.parent != Path("."):
                path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

            self._connection = sqlite3.connect(
                str(path),
                check_same_thread=False,
            )

            self._connection.row_factory = sqlite3.Row

            return {
                "success": True,
                "status": "CONNECTED",
                "database": self.database_path,
            }

    def disconnect(self) -> dict:
        """Close the database connection."""

        with self._lock:
            if self._connection is None:
                return {
                    "success": True,
                    "status": "ALREADY_DISCONNECTED",
                }

            self._connection.close()
            self._connection = None

            return {
                "success": True,
                "status": "DISCONNECTED",
            }

    # ------------------------------------------------------------------
    # INITIALIZATION
    # ------------------------------------------------------------------

    def initialize(self) -> dict:
        """Initialize the database foundation."""

        self.connect()

        self.execute(
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

        self.execute(
            """
            INSERT OR IGNORE INTO system_metadata
            (key, value)
            VALUES (?, ?)
            """,
            (
                "database_version",
                "1.0",
            ),
        )

        return {
            "success": True,
            "status": "READY",
            "database": self.database_path,
        }

    # ------------------------------------------------------------------
    # INTERNAL CONNECTION
    # ------------------------------------------------------------------

    def _require_connection(self) -> sqlite3.Connection:
        """Return an active connection."""

        if self._connection is None:
            self.connect()

        if self._connection is None:
            raise RuntimeError(
                "Database connection could not be established."
            )

        return self._connection

    # ------------------------------------------------------------------
    # EXECUTION
    # ------------------------------------------------------------------

    def execute(
        self,
        query: str,
        parameters: Sequence[Any] | Iterable[Any] = (),
    ) -> int:
        """Execute one SQL statement and return affected rows."""

        with self._lock:
            connection = self._require_connection()

            cursor = connection.cursor()

            try:
                cursor.execute(
                    query,
                    tuple(parameters),
                )

                connection.commit()

                return cursor.rowcount

            except Exception:
                connection.rollback()
                raise

            finally:
                cursor.close()

    def executemany(
        self,
        query: str,
        parameters: Iterable[Sequence[Any]],
    ) -> int:
        """Execute one SQL statement against multiple parameter sets."""

        with self._lock:
            connection = self._require_connection()

            cursor = connection.cursor()

            try:
                cursor.executemany(
                    query,
                    [tuple(item) for item in parameters],
                )

                connection.commit()

                return cursor.rowcount

            except Exception:
                connection.rollback()
                raise

            finally:
                cursor.close()

    # ------------------------------------------------------------------
    # QUERIES
    # ------------------------------------------------------------------

    def fetchone(
        self,
        query: str,
        parameters: Sequence[Any] | Iterable[Any] = (),
    ) -> Optional[sqlite3.Row]:
        """Return one database row."""

        with self._lock:
            connection = self._require_connection()

            cursor = connection.cursor()

            try:
                cursor.execute(
                    query,
                    tuple(parameters),
                )

                return cursor.fetchone()

            finally:
                cursor.close()

    def fetchall(
        self,
        query: str,
        parameters: Sequence[Any] | Iterable[Any] = (),
    ) -> list[sqlite3.Row]:
        """Return all database rows."""

        with self._lock:
            connection = self._require_connection()

            cursor = connection.cursor()

            try:
                cursor.execute(
                    query,
                    tuple(parameters),
                )

                return cursor.fetchall()

            finally:
                cursor.close()

    # ------------------------------------------------------------------
    # TRANSACTION
    # ------------------------------------------------------------------

    def begin(self) -> dict:
        """Begin a transaction."""

        with self._lock:
            connection = self._require_connection()

            connection.execute("BEGIN")

            return {
                "success": True,
                "status": "TRANSACTION_STARTED",
            }

    def commit(self) -> dict:
        """Commit the active transaction."""

        with self._lock:
            connection = self._require_connection()

            connection.commit()

            return {
                "success": True,
                "status": "TRANSACTION_COMMITTED",
            }

    def rollback(self) -> dict:
        """Rollback the active transaction."""

        with self._lock:
            connection = self._require_connection()

            connection.rollback()

            return {
                "success": True,
                "status": "TRANSACTION_ROLLED_BACK",
            }

    # ------------------------------------------------------------------
    # HEALTH
    # ------------------------------------------------------------------

    def health(self) -> dict:
        """Return database health information."""

        try:
            self._require_connection()

            self.fetchone(
                "SELECT 1"
            )

            return {
                "success": True,
                "status": "HEALTHY",
                "connected": True,
                "database": self.database_path,
            }

        except Exception as exc:
            return {
                "success": False,
                "status": "UNHEALTHY",
                "connected": False,
                "database": self.database_path,
                "error": str(exc),
            }

    # ------------------------------------------------------------------
    # INFORMATION
    # ------------------------------------------------------------------

    def status(self) -> dict:
        """Return database service status."""

        return {
            "service": "DatabaseService",
            "database": self.database_path,
            "connected": self._connection is not None,
        }


__all__ = [
    "DatabaseService",
]
