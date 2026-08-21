"""MAIN BASE FOUNDATION database engine."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional


class DatabaseEngine:
    """Central database engine for MAIN BASE FOUNDATION."""

    def __init__(
        self,
        database_url: str = "sqlite:///main_base_foundation.db",
    ):
        self.database_url = database_url
        self.status = "READY"
        self.connected = False
        self.last_check = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

    def connect(self) -> dict:
        """Register database connectivity state."""

        self.connected = True
        self.status = "CONNECTED"
        self.last_check = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        return self.status()

    def disconnect(self) -> dict:
        """Disconnect the database engine."""

        self.connected = False
        self.status = "DISCONNECTED"
        self.last_check = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        return self.status()

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
            "status": self.status,
            "connected": self.connected,
            "database_url": self._safe_database_url(),
            "last_check": self.last_check,
        }

    def ping(self) -> dict:
        """Perform a lightweight database availability check."""

        self.last_check = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        return {
            "database": "MAIN BASE FOUNDATION",
            "reachable": self.connected,
            "status": (
                "ONLINE"
                if self.connected
                else "OFFLINE"
            ),
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

        if self.database_url.startswith(
            "sqlite"
        ):
            return "SQLITE"

        if self.database_url.startswith(
            "postgresql"
        ):
            return "POSTGRESQL"

        if self.database_url.startswith(
            "mysql"
        ):
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
