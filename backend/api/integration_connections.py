"""MAIN BASE FOUNDATION integration connection API."""

from backend.engines.integrations.connections import (
    IntegrationConnectionManager,
)


class IntegrationConnectionsAPI:
    """API facade for provider connection lifecycle."""

    def __init__(self):
        self.manager = IntegrationConnectionManager()

    def connect(
        self,
        provider: str,
    ) -> dict:
        """Connect an explicitly authorized provider."""

        return self.manager.connect(provider)

    def disconnect(
        self,
        provider: str,
    ) -> dict:
        """Disconnect a provider."""

        return self.manager.disconnect(provider)

    def status(
        self,
        provider: str,
    ) -> dict:
        """Return one provider connection status."""

        return self.manager.status(provider)

    def statuses(self) -> list:
        """Return all provider connection statuses."""

        return self.manager.statuses()

    def health(self) -> dict:
        """Return global connection health."""

        return self.manager.health()
