"""MAIN BASE FOUNDATION provider connection lifecycle."""

from datetime import datetime, timezone
from typing import Dict, List

from .registry import IntegrationRegistry
from .security import IntegrationSecurity


class IntegrationConnectionManager:
    """Manage safe provider connection state.

    This class does not store provider secrets.
    """

    def __init__(self):
        self.registry = IntegrationRegistry()
        self.connections: Dict[str, dict] = {}

    def connect(
        self,
        provider: str,
    ) -> dict:
        """Mark an explicitly authorized provider as connected."""

        normalized = IntegrationSecurity.validate_provider(
            provider
        )

        definition = self.registry.get(normalized)

        self.connections[normalized] = {
            "provider": definition.provider,
            "status": "CONNECTED",
            "authenticated": True,
            "connected_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        return self.status(normalized)

    def disconnect(
        self,
        provider: str,
    ) -> dict:
        """Disconnect a provider from the local integration state."""

        normalized = IntegrationSecurity.validate_provider(
            provider
        )

        self.registry.get(normalized)

        self.connections.pop(
            normalized,
            None,
        )

        return {
            "provider": normalized,
            "status": "DISCONNECTED",
            "authenticated": False,
        }

    def status(
        self,
        provider: str,
    ) -> dict:
        """Return safe connection state."""

        normalized = IntegrationSecurity.validate_provider(
            provider
        )

        definition = self.registry.get(normalized)

        connection = self.connections.get(
            normalized
        )

        if connection:
            return {
                "provider": normalized,
                "category": definition.category,
                "status": connection["status"],
                "authenticated": True,
                "connected_at": connection[
                    "connected_at"
                ],
            }

        return {
            "provider": normalized,
            "category": definition.category,
            "status": "NOT_CONNECTED",
            "authenticated": False,
            "connected_at": None,
        }

    def statuses(self) -> List[dict]:
        """Return safe connection state for all providers."""

        return [
            self.status(
                definition.provider
            )
            for definition in (
                self.registry.definitions.values()
            )
        ]

    def health(self) -> dict:
        """Return connection health summary."""

        statuses = self.statuses()

        connected = sum(
            item["status"] == "CONNECTED"
            for item in statuses
        )

        return {
            "status": (
                "CONNECTED"
                if connected
                else "NO_ACTIVE_CONNECTIONS"
            ),
            "providers": len(statuses),
            "connected": connected,
            "disconnected": (
                len(statuses) - connected
            ),
        }
