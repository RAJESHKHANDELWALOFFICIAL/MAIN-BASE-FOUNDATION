"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Provider Connector Registry

Central registry for external platform connectors.

The registry:
- Registers provider connectors
- Returns a connector for a provider
- Lists registered providers
- Keeps provider-specific logic outside IntegrationService
"""

from __future__ import annotations

from typing import Dict, List, Optional

from backend.supreme.ecosystem.connectors.base import (
    EcosystemProviderConnector,
)
from backend.supreme.ecosystem.integration.model import (
    IntegrationProvider,
)


class ConnectorRegistry:
    """Central registry for SUPREME ecosystem connectors."""

    def __init__(self) -> None:

        self._connectors: Dict[
            IntegrationProvider,
            EcosystemProviderConnector,
        ] = {}

    # =========================================================
    # 🔌 REGISTER
    # =========================================================

    def register(
        self,
        connector: EcosystemProviderConnector,
    ) -> EcosystemProviderConnector:
        """Register a provider connector."""

        provider = connector.provider

        if provider in self._connectors:
            raise ValueError(
                f"Connector already registered for "
                f"{provider.value}."
            )

        self._connectors[provider] = connector

        return connector

    # =========================================================
    # 🔎 GET
    # =========================================================

    def get(
        self,
        provider: IntegrationProvider,
    ) -> Optional[EcosystemProviderConnector]:
        """Return a registered provider connector."""

        return self._connectors.get(provider)

    # =========================================================
    # 📋 LIST
    # =========================================================

    def list_providers(
        self,
    ) -> List[IntegrationProvider]:
        """Return all registered providers."""

        return list(self._connectors.keys())

    # =========================================================
    # ❓ EXISTS
    # =========================================================

    def has(
        self,
        provider: IntegrationProvider,
    ) -> bool:
        """Check whether a provider is registered."""

        return provider in self._connectors

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return registry status."""

        return {
            "registry": (
                "SUPREME_ECOSYSTEM_CONNECTOR"
            ),
            "connectors": len(
                self._connectors
            ),
            "providers": [
                provider.value
                for provider in self._connectors
            ],
        }


__all__ = [
    "ConnectorRegistry",
]
