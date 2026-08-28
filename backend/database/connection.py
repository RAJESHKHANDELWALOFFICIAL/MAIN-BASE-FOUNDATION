"""MAIN BASE FOUNDATION database connection.

Low-level SQLite connection management for the database layer.

This module is responsible only for creating, maintaining, checking,
and closing the SQLite database connection.

Higher-level database operations remain in DatabaseService.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from threading import RLock
from typing import Optional


class DatabaseConnection:
    """Manage the SQLite connection used by MAIN BASE FOUNDATION."""

    def __init__(
        self,
        database_name: str = "main_base_foundation.db",
        timeout: float = 30.0,
    ) -> None:
        self.database_name = database_name
        self.timeout = timeout

        self.connection: Optional[sqlite3.Connection] = None
        self._lock = RLock()

    # ------------------------------------------------------------------
    # CONNECTION
    # ------------------------------------------------------------------

    def connect(self) -> sqlite3.Connection:
        """Create and return an active SQLite connection."""

        with self._lock:
            if self.connection is not None:
                return self.connection

            path = Path(self.database_name)

            if path.parent != Path("."):
                path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

            self.connection = sqlite3.connect(
                str(path),
                timeout=self.timeout,
                check_same_thread=False,
            )

            self.connection.row_factory = sqlite3.Row

            return self.connection

    # ------------------------------------------------------------------
    # CLOSE
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the active database connection."""

        with self._lock:
            if self.connection is None:
                return

            self.connection.close()
            self.connection = None

    # ------------------------------------------------------------------
    # STATUS
    # ------------------------------------------------------------------

    def is_connected(self) -> bool:
        """Return whether a database connection is currently active."""

        with self._lock:
            return self.connection is not None

    def database(self) -> str:
        """Return the configured database path."""

        return self.database_name

    def status(self) -> dict:
        """Return safe connection status information."""

        return {
            "database": self.database_name,
            "connected": self.is_connected(),
            "timeout": self.timeout,
        }

    # ------------------------------------------------------------------
    # HEALTH
    # ------------------------------------------------------------------

    def health(self) -> dict:
        """Check whether the active database connection is healthy."""

        with self._lock:
            if self.connection is None:
                return {
                    "success": False,
                    "status": "DISCONNECTED",
                    "database": self.database_name,
                    "connected": False,
                }

            try:
                self.connection.execute(
                    "SELECT 1"
                )

                return {
                    "success": True,
                    "status": "HEALTHY",
                    "database": self.database_name,
                    "connected": True,
                }

            except sqlite3.Error as exc:
                return {
                    "success": False,
                    "status": "UNHEALTHY",
                    "database": self.database_name,
                    "connected": False,
                    "error": str(exc),
                }


__all__ = [
    "DatabaseConnection",
]
