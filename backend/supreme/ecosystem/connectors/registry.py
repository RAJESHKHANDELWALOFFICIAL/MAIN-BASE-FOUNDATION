"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Provider Connector Registry

Central registry for external provider connectors.

Responsibilities:
- Register provider connectors.
- Retrieve a connector by provider key.
- List registered providers.
- Prevent accidental duplicate registration.
- Keep provider implementations separate from the core ecosystem.

Security principles:
- Registry never stores passwords.
- Registry never stores OTPs.
- Registry never exposes raw credentials.
- Provider authorization remains provider-controlled.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from backend.supreme.ecosystem.connectors.base import (
    EcosystemProviderConnector,
)


class ConnectorRegistry:
    """
    Central registry for SUPREME provider connectors.
    """

    def __init__(self) -> None:

        self._connectors: Dict[
            str,
            EcosystemProviderConnector,
        ] = {}

    # =========================================================
    # ➕ REGISTER
    # =========================================================

    def register(
        self,
        connector: EcosystemProviderConnector,
    ) -> None:
        """
        Register a provider connector.
        """

        provider_key = (
            connector.provider_key.strip().lower()
        )

        if not provider_key:
            raise ValueError(
                "Connector provider_key cannot be empty."
            )

        if provider_key in self._connectors:
            raise ValueError(
                f"Connector already registered: "
                f"{provider_key}"
            )

        self._connectors[provider_key] = connector

    # =========================================================
    # 🔎 GET
    # =========================================================

    def get(
        self,
        provider_key: str,
    ) -> Optional[
        EcosystemProviderConnector
    ]:
        """
        Return a registered connector.
        """

        key = provider_key.strip().lower()

        return self._connectors.get(key)

    # =========================================================
    # ✅ REQUIRE
    # =========================================================

    def require(
        self,
        provider_key: str,
    ) -> EcosystemProviderConnector:
        """
        Return a connector or raise an explicit error.
        """

        connector = self.get(
            provider_key
        )

        if connector is None:
            raise KeyError(
                f"No connector registered for provider: "
                f"{provider_key}"
            )

        return connector

    # =========================================================
    # 📋 LIST
    # =========================================================

    def list_providers(self) -> List[str]:
        """
        Return registered provider keys.
        """

        return sorted(
            self._connectors.keys()
        )

    # =========================================================
    # 🔢 COUNT
    # =========================================================

    def count(self) -> int:
        """
        Return number of registered connectors.
        """

        return len(
            self._connectors
        )

    # =========================================================
    # ❓ EXISTS
    # =========================================================

    def contains(
        self,
        provider_key: str,
    ) -> bool:
        """
        Check whether a provider is registered.
        """

        key = provider_key.strip().lower()

        return key in self._connectors

    # =========================================================
    # 🧹 CLEAR
    # =========================================================

    def clear(self) -> None:
        """
        Remove all registered connectors.

        Intended for controlled initialization/testing.
        """

        self._connectors.clear()


__all__ = [
    "ConnectorRegistry",
]
