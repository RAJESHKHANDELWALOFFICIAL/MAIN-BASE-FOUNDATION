"""MAIN BASE FOUNDATION connection manager."""

from typing import Dict

from .models import Connection


class ConnectionManager:
    """Manage authorized provider and server connections."""

    def __init__(self):
        self.connections: Dict[str, Connection] = {}

    def register(
        self,
        connection_id: str,
        provider_id: str,
        server_id: str,
        connection_type: str,
        protocol: str,
        endpoint: str | None = None,
    ) -> dict:
        """Register a connection."""

        if connection_id in self.connections:
            return {
                "success": False,
                "error": "CONNECTION_ID_ALREADY_EXISTS",
                "connection_id": connection_id,
            }

        connection = Connection(
            connection_id=connection_id,
            provider_id=provider_id,
            server_id=server_id,
            connection_type=connection_type,
            protocol=protocol,
            endpoint=endpoint,
        )

        self.connections[connection_id] = connection

        return {
            "success": True,
            "connection": connection.__dict__,
        }

    def get(
        self,
        connection_id: str,
    ) -> dict:
        """Return one connection."""

        connection = self.connections.get(connection_id)

        if connection is None:
            return {
                "success": False,
                "error": "CONNECTION_NOT_FOUND",
                "connection_id": connection_id,
            }

        return {
            "success": True,
            "connection": connection.__dict__,
        }

    def list(self) -> dict:
        """Return all connections."""

        return {
            "success": True,
            "count": len(self.connections),
            "connections": [
                connection.__dict__
                for connection in self.connections.values()
            ],
        }

    def authorize(
        self,
        connection_id: str,
    ) -> dict:
        """Authorize a connection."""

        connection = self.connections.get(connection_id)

        if connection is None:
            return {
                "success": False,
                "error": "CONNECTION_NOT_FOUND",
            }

        connection.authorized = True
        connection.status = "AUTHORIZED"
        connection.error = None

        return {
            "success": True,
            "connection": connection.__dict__,
        }

    def connect(
        self,
        connection_id: str,
    ) -> dict:
        """Establish an authorized connection."""

        connection = self.connections.get(connection_id)

        if connection is None:
            return {
                "success": False,
                "error": "CONNECTION_NOT_FOUND",
            }

        if not connection.authorized:
            return {
                "success": False,
                "error": "CONNECTION_NOT_AUTHORIZED",
                "connection_id": connection_id,
            }

        if not connection.enabled:
            return {
                "success": False,
                "error": "CONNECTION_DISABLED",
                "connection_id": connection_id,
            }

        connection.status = "CONNECTED"
        connection.error = None

        return {
            "success": True,
            "connection": connection.__dict__,
        }

    def disconnect(
        self,
        connection_id: str,
    ) -> dict:
        """Disconnect a connection."""

        connection = self.connections.get(connection_id)

        if connection is None:
            return {
                "success": False,
                "error": "CONNECTION_NOT_FOUND",
            }

        connection.status = "DISCONNECTED"

        return {
            "success": True,
            "connection": connection.__dict__,
        }

    def disable(
        self,
        connection_id: str,
    ) -> dict:
        """Disable a connection."""

        connection = self.connections.get(connection_id)

        if connection is None:
            return {
                "success": False,
                "error": "CONNECTION_NOT_FOUND",
            }

        connection.enabled = False
        connection.status = "DISABLED"

        return {
            "success": True,
            "connection": connection.__dict__,
        }

    def health(self) -> dict:
        """Return connection system health."""

        connected = sum(
            1
            for connection in self.connections.values()
            if connection.status == "CONNECTED"
        )

        return {
            "system": "Connection Manager",
            "health": "HEALTHY",
            "registered_connections": len(
                self.connections
            ),
            "connected": connected,
        }
