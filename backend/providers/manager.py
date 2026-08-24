"""MAIN BASE FOUNDATION provider registry."""

from typing import Dict

from .models import Provider


class ProviderManager:
    """Manage registered infrastructure providers."""

    def __init__(self):
        self.providers: Dict[str, Provider] = {}

    def register(
        self,
        provider_id: str,
        provider_name: str,
        provider_type: str,
        country: str,
        region: str,
        environment: str,
        website: str | None = None,
        api_endpoint: str | None = None,
        authorized: bool = False,
    ) -> dict:
        """Register a provider."""

        if provider_id in self.providers:
            return {
                "success": False,
                "error": "PROVIDER_ID_ALREADY_EXISTS",
                "provider_id": provider_id,
            }

        provider = Provider(
            provider_id=provider_id,
            provider_name=provider_name,
            provider_type=provider_type,
            country=country,
            region=region,
            environment=environment,
            website=website,
            api_endpoint=api_endpoint,
            authorized=authorized,
        )

        self.providers[provider_id] = provider

        return {
            "success": True,
            "provider": provider.__dict__,
        }

    def get(self, provider_id: str) -> dict:
        """Return one provider."""

        provider = self.providers.get(provider_id)

        if provider is None:
            return {
                "success": False,
                "error": "PROVIDER_NOT_FOUND",
                "provider_id": provider_id,
            }

        return {
            "success": True,
            "provider": provider.__dict__,
        }

    def list(self) -> dict:
        """Return all registered providers."""

        return {
            "success": True,
            "count": len(self.providers),
            "providers": [
                provider.__dict__
                for provider in self.providers.values()
            ],
        }

    def authorize(self, provider_id: str) -> dict:
        """Authorize a provider."""

        provider = self.providers.get(provider_id)

        if provider is None:
            return {
                "success": False,
                "error": "PROVIDER_NOT_FOUND",
            }

        provider.authorized = True
        provider.status = "AUTHORIZED"

        return {
            "success": True,
            "provider": provider.__dict__,
        }

    def disable(self, provider_id: str) -> dict:
        """Disable a provider."""

        provider = self.providers.get(provider_id)

        if provider is None:
            return {
                "success": False,
                "error": "PROVIDER_NOT_FOUND",
            }

        provider.enabled = False
        provider.status = "DISABLED"

        return {
            "success": True,
            "provider": provider.__dict__,
        }

    def health(self) -> dict:
        """Return provider registry health."""

        return {
            "system": "Provider Registry",
            "health": "HEALTHY",
            "registered_providers": len(self.providers),
        }
