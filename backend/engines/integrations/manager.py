"""MAIN BASE FOUNDATION global integrations manager."""

from typing import Dict, List

from .registry import IntegrationRegistry


class IntegrationManager:
    """Manage registered external integrations without storing secrets."""

    def __init__(self):
        self.registry = IntegrationRegistry()

    def definitions(self) -> List[dict]:
        """Return all registered integration definitions."""

        return self.registry.list()

    def statuses(self) -> List[dict]:
        """Return safe integration readiness status."""

        return self.registry.statuses()

    def status(self, provider: str) -> dict:
        """Return safe status for one provider."""

        return self.registry.status(provider).to_dict()

    def health(self) -> dict:
        """Return global integration health summary."""

        statuses = self.statuses()

        ready = sum(
            item["status"] == "READY_FOR_AUTHORIZATION"
            for item in statuses
        )

        return {
            "status": "READY_FOR_AUTHORIZATION",
            "providers": len(statuses),
            "ready_for_authorization": ready,
            "authenticated": sum(
                item["authenticated"]
                for item in statuses
            ),
            "configured": sum(
                item["configured"]
                for item in statuses
            ),
        }

    def authorization_requirements(
        self,
        provider: str,
    ) -> Dict[str, object]:
        """Return requirements before connecting a provider."""

        definition = self.registry.get(provider)

        return {
            "provider": definition.provider,
            "authentication": definition.authentication,
            "requires_credentials": (
                definition.requires_credentials
            ),
            "official_api": definition.official_api,
            "capabilities": definition.capabilities,
            "status": "AUTHORIZATION_REQUIRED",
        }
