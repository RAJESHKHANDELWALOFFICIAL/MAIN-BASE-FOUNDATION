"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Connector Manager

Central lifecycle manager for provider connectors.

Responsibilities:
- Initialize the connector registry.
- Register built-in connectors.
- Expose connector lookup.
- Expose connector status.
- Keep provider authentication inside provider connectors.

Security:
- No plaintext passwords.
- No OTP storage.
- No raw secrets.
- No authentication bypass.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base import EcosystemProviderConnector
from .registry import (
    ConnectorRegistry,
    registry as default_connector_registry,
)

from .providers.registration import (
    register_builtin_connectors,
)


class ConnectorManager:
    """Central SUPREME connector lifecycle manager."""

    def __init__(
        self,
        connector_registry: Optional[
            ConnectorRegistry
        ] = None,
    ) -> None:

        self.registry = (
            connector_registry
            if connector_registry is not None
            else default_connector_registry
        )

        self._initialized = False

    # =====================================================
    # 🚀 INITIALIZE
    # =====================================================

    def initialize(self) -> Dict[str, Any]:
        """
        Initialize and register built-in connectors.
        """

        if not self._initialized:
            register_builtin_connectors(
                self.registry
            )

            self._initialized = True

        return {
            "manager": (
                "SUPREME_ECOSYSTEM_CONNECTOR_MANAGER"
            ),
            "status": "READY",
            "initialized": True,
            "connector_count": self.registry.count(),
            "providers": self.registry.providers(),
        }

    # =====================================================
    # 🔎 GET CONNECTOR
    # =====================================================

    def get_connector(
        self,
        provider_id: str,
    ) -> Optional[EcosystemProviderConnector]:
        """Return a registered connector."""

        if not self._initialized:
            self.initialize()

        return self.registry.get(
            provider_id
        )

    # =====================================================
    # ✅ EXISTS
    # =====================================================

    def has_connector(
        self,
        provider_id: str,
    ) -> bool:
        """Check whether a connector exists."""

        if not self._initialized:
            self.initialize()

        return self.registry.exists(
            provider_id
        )

    # =====================================================
    # 📋 PROVIDERS
    # =====================================================

    def providers(self) -> List[str]:
        """Return registered providers."""

        if not self._initialized:
            self.initialize()

        return self.registry.providers()

    # =====================================================
    # ❤️ HEALTH
    # =====================================================

    def health_check(
        self,
        provider_id: str,
    ):
        """Run a safe health check."""

        connector = self.get_connector(
            provider_id
        )

        if connector is None:
            raise ValueError(
                "Provider connector is not registered: "
                f"{provider_id}"
            )

        return connector.health_check()

    # =====================================================
    # 📊 STATUS
    # =====================================================

    def status(self) -> Dict[str, Any]:
        """Return safe manager status."""

        if not self._initialized:
            self.initialize()

        return {
            "manager": (
                "SUPREME_ECOSYSTEM_CONNECTOR_MANAGER"
            ),
            "initialized": self._initialized,
            "connector_count": self.registry.count(),
            "providers": self.registry.providers(),
        }


# =========================================================
# 🌍 DEFAULT MANAGER
# =========================================================

connector_manager = ConnectorManager()


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "ConnectorManager",
    "connector_manager",
]
