"""
MAIN BASE FOUNDATION
Central Database Engine

Provides persistent database connectivity and
storage services for MAIN-BASE-FOUNDATION.
"""

from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from typing import Any, Dict, Optional


class DatabaseEngine:
    """Central database engine for MAIN BASE FOUNDATION."""

    def __init__(
        self,
        database_url: str = "sqlite:///main_base_foundation.db",
    ):
        self.database_url = database_url
        self._status = "READY"
        self.connected = False
        self.last_check = self._now()

        self.connection: Optional[sqlite3.Connection] = None

    def _now(self) -> str:
        """Return current UTC timestamp."""

        return datetime.now(timezone.utc).isoformat()

    def connect(self) -> dict:
        """Connect to the configured database."""

        if self.connected and self.connection is not None:
            return self.status()

        if not self.database_url.startswith("sqlite:///"):
            raise NotImplementedError(
                "Only SQLite is currently supported."
            )

        database_path = self.database_url.replace(
            "sqlite:///",
            "",
            1,
        )

        path = Path(database_path)

        if not path.is_absolute():
            path = Path.cwd() / path

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            str(path),
            check_same_thread=False,
        )

        self.connection.row_factory = sqlite3.Row

        self.connected = True
        self._status = "CONNECTED"
        self.last_check = self._now()

        return self.status()

    def disconnect(self) -> dict:
        """Disconnect the database engine."""

        if self.connection is not None:
            self.connection.close()

        self.connection = None
        self.connected = False
        self._status = "DISCONNECTED"
        self.last_check = self._now()

        return self.status()

    def ensure_connected(self) -> sqlite3.Connection:
        """Return an active database connection."""

        if not self.connected or self.connection is None:
            self.connect()

        if self.connection is None:
            raise RuntimeError(
                "Database connection could not be established."
            )

        return self.connection

    def execute(
        self,
        query: str,
        parameters: tuple = (),
    ) -> sqlite3.Cursor:
        """Execute a SQL statement."""

        connection = self.ensure_connected()

        cursor = connection.execute(
            query,
            parameters,
        )

        connection.commit()

        self.last_check = self._now()

        return cursor

    def executemany(
        self,
        query: str,
        parameters: list[tuple],
    ) -> sqlite3.Cursor:
        """Execute a SQL statement against multiple parameter sets."""

        connection = self.ensure_connected()

        cursor = connection.executemany(
            query,
            parameters,
        )

        connection.commit()

        self.last_check = self._now()

        return cursor

    def fetch_one(
        self,
        query: str,
        parameters: tuple = (),
    ) -> Optional[dict]:
        """Fetch one database record."""

        connection = self.ensure_connected()

        cursor = connection.execute(
            query,
            parameters,
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    def fetch_all(
        self,
        query: str,
        parameters: tuple = (),
    ) -> list[dict]:
        """Fetch all database records."""

        connection = self.ensure_connected()

        cursor = connection.execute(
            query,
            parameters,
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    def create_table(
        self,
        query: str,
    ) -> None:
        """Create a database table."""

        self.execute(query)

    def health(self) -> dict:
        """Return database health information."""

        if self.connected:
            health = "HEALTHY"
        else:
            health = "READY"

        return {
            "database": "MAIN BASE FOUNDATION",
            "health": health,
            "connected": self.connected,
            "database_url": self._safe_database_url(),
            "last_check": self.last_check,
        }

    def status(self) -> dict:
        """Return current database status."""

        return {
            "database": "MAIN BASE FOUNDATION",
            "status": self._status,
            "connected": self.connected,
            "database_url": self._safe_database_url(),
            "last_check": self.last_check,
        }

    def ping(self) -> dict:
        """Perform a lightweight database availability check."""

        self.last_check = self._now()

        if not self.connected:
            return {
                "database": "MAIN BASE FOUNDATION",
                "reachable": False,
                "status": "OFFLINE",
                "last_check": self.last_check,
            }

        try:
            self.execute("SELECT 1")

            return {
                "database": "MAIN BASE FOUNDATION",
                "reachable": True,
                "status": "ONLINE",
                "last_check": self.last_check,
            }

        except Exception:
            return {
                "database": "MAIN BASE FOUNDATION",
                "reachable": False,
                "status": "OFFLINE",
                "last_check": self.last_check,
            }

    def configuration(self) -> dict:
        """Return non-secret database configuration."""

        return {
            "engine": "DATABASE",
            "database_url": self._safe_database_url(),
            "driver": self._driver_name(),
            "secret_storage": False,
        }

    def _driver_name(self) -> str:
        """Return the configured database driver."""

        if self.database_url.startswith("sqlite"):
            return "SQLITE"

        if self.database_url.startswith("postgresql"):
            return "POSTGRESQL"

        if self.database_url.startswith("mysql"):
            return "MYSQL"

        return "UNKNOWN"

    def _safe_database_url(self) -> str:
        """Return database URL without exposed credentials."""

        value = self.database_url

        if "@" in value and "://" in value:
            prefix, remainder = value.split(
                "://",
                1,
            )

            if "@" in remainder:
                credentials, host = remainder.split(
                    "@",
                    1,
                )

                if ":" in credentials:
                    username = credentials.split(
                        ":",
                        1,
                    )[0]

                    return (
                        f"{prefix}://"
                        f"{username}:***@{host}"
                    )

        return value


__all__ = [
    "DatabaseEngine",
]
