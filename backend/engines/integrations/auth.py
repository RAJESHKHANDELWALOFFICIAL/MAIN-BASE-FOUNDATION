"""MAIN BASE FOUNDATION integration authorization manager."""

from typing import Dict, List

from .registry import IntegrationRegistry
from .security import IntegrationSecurity


class IntegrationAuthorization:
    """Manage provider authorization metadata and OAuth state."""

    def __init__(self):
        self.registry = IntegrationRegistry()

    def providers(self) -> List[dict]:
        """Return providers that support authorization."""

        result = []

        for definition in self.registry.definitions.values():
            result.append(
                {
                    "provider": definition.provider,
                    "authentication": definition.authentication,
                    "official_api": definition.official_api,
                    "requires_credentials": (
                        definition.requires_credentials
                    ),
                    "capabilities": definition.capabilities,
                }
            )

        return result

    def requirements(
        self,
        provider: str,
    ) -> Dict[str, object]:
        """Return authorization requirements for a provider."""

        normalized = IntegrationSecurity.validate_provider(
            provider
        )

        definition = self.registry.get(normalized)

        return {
            "provider": definition.provider,
            "authentication": definition.authentication,
            "official_api": definition.official_api,
            "requires_credentials": (
                definition.requires_credentials
            ),
            "capabilities": definition.capabilities,
            "authorization": "EXPLICIT_USER_AUTHORIZATION_REQUIRED",
        }

    def create_state(
        self,
        provider: str,
    ) -> Dict[str, str]:
        """Create an OAuth state value for an authorization attempt."""

        normalized = IntegrationSecurity.validate_provider(
            provider
        )

        self.registry.get(normalized)

        return {
            "provider": normalized,
            "state": IntegrationSecurity.generate_state(),
            "status": "AUTHORIZATION_STATE_CREATED",
        }

    def revoke_instructions(
        self,
        provider: str,
    ) -> Dict[str, object]:
        """Return safe provider disconnect metadata."""

        normalized = IntegrationSecurity.validate_provider(
            provider
        )

        definition = self.registry.get(normalized)

        return {
            "provider": definition.provider,
            "status": "REVOCATION_REQUIRED",
            "message": (
                "Provider credentials must be revoked "
                "through the provider's authorized account "
                "or official API flow."
            ),
        }
