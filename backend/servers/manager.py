"""MAIN BASE FOUNDATION server registry."""

from typing import Dict

from .models import Server


class ServerManager:
    """Manage authorized server registrations."""

    def __init__(self):
        self.servers: Dict[str, Server] = {}

    def register(
        self,
        server_id: str,
        server_name: str,
        provider_id: str,
        server_type: str,
        server_role: str,
        country: str,
        region: str,
        environment: str,
        authorized: bool = False,
        endpoint: str | None = None,
        protocol: str | None = None,
    ) -> dict:
        """Register a server."""

        if server_id in self.servers:
            return {
                "success": False,
                "error": "SERVER_ID_ALREADY_EXISTS",
                "server_id": server_id,
            }

        server = Server(
            server_id=server_id,
            server_name=server_name,
            provider_id=provider_id,
            server_type=server_type,
            server_role=server_role,
            country=country,
            region=region,
            environment=environment,
            authorized=authorized,
            endpoint=endpoint,
            protocol=protocol,
        )

        self.servers[server_id] = server

        return {
            "success": True,
            "server": server.__dict__,
        }

    def get(self, server_id: str) -> dict:
        """Return one server."""

        server = self.servers.get(server_id)

        if server is None:
            return {
                "success": False,
                "error": "SERVER_NOT_FOUND",
                "server_id": server_id,
            }

        return {
            "success": True,
            "server": server.__dict__,
        }

    def list(self) -> dict:
        """Return registered servers."""

        return {
            "success": True,
            "count": len(self.servers),
            "servers": [
                server.__dict__
                for server in self.servers.values()
            ],
        }

    def health(self) -> dict:
        """Return server registry health."""

        return {
            "system": "Server Registry",
            "health": "HEALTHY",
            "registered_servers": len(self.servers),
        }

    def authorize(self, server_id: str) -> dict:
        """Mark a server as authorized."""

        server = self.servers.get(server_id)

        if server is None:
            return {
                "success": False,
                "error": "SERVER_NOT_FOUND",
            }

        server.authorized = True
        server.status = "AUTHORIZED"

        return {
            "success": True,
            "server": server.__dict__,
        }

    def disable(self, server_id: str) -> dict:
        """Disable a registered server."""

        server = self.servers.get(server_id)

        if server is None:
            return {
                "success": False,
                "error": "SERVER_NOT_FOUND",
            }

        server.enabled = False
        server.status = "DISABLED"

        return {
            "success": True,
            "server": server.__dict__,
        }
