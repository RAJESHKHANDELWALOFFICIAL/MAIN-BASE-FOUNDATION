from backend.engines.integrations.manager import IntegrationManager


class IntegrationsAPI:
    """MAIN BASE FOUNDATION Global Integrations API."""

    def __init__(self):
        self.manager = IntegrationManager()

    def definitions(self) -> list:
        """Return registered integration definitions."""

        return self.manager.definitions()

    def statuses(self) -> list:
        """Return safe integration readiness statuses."""

        return self.manager.statuses()

    def health(self) -> dict:
        """Return global integration health."""

        return self.manager.health()

    def status(self, provider: str) -> dict:
        """Return one provider status."""

        return self.manager.status(provider)

    def authorization_requirements(
        self,
        provider: str,
    ) -> dict:
        """Return authorization requirements."""

        return self.manager.authorization_requirements(
            provider
        )
