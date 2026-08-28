"""
MAIN BASE FOUNDATION
SUPREME — Database Connection Layer

Central database connection access for SUPREME.

This layer keeps database connectivity separate from:
- authentication
- authorization
- business logic
- AI
- Vault
- MUKTI MAHAL
- external integrations
"""

from typing import Any, Optional

from backend.database.connection import DatabaseConnection


class SupremeConnection:
    """
    Central database connection manager for SUPREME.
    """

    def __init__(self) -> None:
        self._database: Optional[Any] = None
        self._connected: bool = False

    # =====================================================
    # 🔌 CONNECT
    # =====================================================

    def connect(self) -> Any:
        """
        Establish and return the SUPREME database connection.
        """

        if self._connected and self._database is not None:
            return self._database

        self._database = (
            DatabaseConnection().connect()
        )

        self._connected = True

        return self._database

    # =====================================================
    # 📡 CONNECTION ACCESS
    # =====================================================

    @property
    def database(self) -> Any:
        """
        Return the active database connection.

        Automatically connects when required.
        """

        if not self._connected:
            return self.connect()

        return self._database

    # =====================================================
    # 🔎 CONNECTION STATUS
    # =====================================================

    @property
    def is_connected(self) -> bool:
        """
        Return whether SUPREME currently has
        an active database connection reference.
        """

        return (
            self._connected
            and self._database is not None
        )

    # =====================================================
    # 🔄 RECONNECT
    # =====================================================

    def reconnect(self) -> Any:
        """
        Reset the current connection reference and
        establish a fresh database connection.
        """

        self._database = None
        self._connected = False

        return self.connect()

    # =====================================================
    # 🔌 DISCONNECT
    # =====================================================

    def disconnect(self) -> None:
        """
        Release the local database connection reference.

        If the underlying database implementation exposes
        a close() method, call it safely.
        """

        if self._database is not None:

            close_method = getattr(
                self._database,
                "close",
                None,
            )

            if callable(close_method):
                close_method()

        self._database = None
        self._connected = False

    # =====================================================
    # 📊 STATUS
    # =====================================================

    def status(self) -> dict:
        """
        Return SUPREME database connection status.
        """

        return {
            "service": "supreme_database",
            "connected": self.is_connected,
        }


__all__ = [
    "SupremeConnection",
]
