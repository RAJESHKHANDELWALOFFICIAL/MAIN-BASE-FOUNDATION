"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Provider Connector Registry

Central registry for authorized ecosystem provider connectors.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Type

from .base import EcosystemProviderConnector


class ConnectorRegistry:
    """
    Central registry for SUPREME ecosystem connectors.
    """

    def __init__(self) -> None:
        self._connectors: Dict[
            str,
            Type[EcosystemProviderConnector],
        ] = {}

    # =====================================================
    # REGISTER
    # =====================================================

    def register(
        self,
        connector_class: Type[EcosystemProviderConnector],
    ) -> Type[EcosystemProviderConnector]:
        """
        Register a provider connector class.
        """

        connector = connector_class()

        provider_id = connector.provider_id()

        if not provider_id:
            raise ValueError(
                "Connector provider_id cannot be empty."
            )

        normalized_id = provider_id.strip().lower()

        if normalized_id in self._connectors:
            raise ValueError(
                f"Connector already registered: {provider_id}"
            )

        self._connectors[
            normalized_id
        ] = connector_class

        return connector_class

    # =====================================================
    # UNREGISTER
    # =====================================================

    def unregister(
        self,
        provider_id: str,
    ) -> bool:
        """
        Remove a registered connector.
        """

        normalized_id = provider_id.strip().lower()

        if normalized_id not in self._connectors:
            return False

        del self._connectors[normalized_id]

        return True

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        provider_id: str,
    ) -> Optional[EcosystemProviderConnector]:
        """
        Return an instantiated connector.

        Returns None when the provider is not registered.
        """

        normalized_id = provider_id.strip().lower()

        connector_class = self._connectors.get(
            normalized_id
        )

        if connector_class is None:
            return None

        return connector_class()

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(
        self,
        provider_id: str,
    ) -> bool:
        """
        Check whether a provider is registered.
        """

        normalized_id = provider_id.strip().lower()

        return normalized_id in self._connectors

    # =====================================================
    # LIST
    # =====================================================

    def providers(self) -> List[str]:
        """
        Return all registered provider identifiers.
        """

        return sorted(
            self._connectors.keys()
        )

    # =====================================================
    # COUNT
    # =====================================================

    def count(self) -> int:
        """
        Return number of registered connectors.
        """

        return len(self._connectors)


# =========================================================
# GLOBAL REGISTRY
# =========================================================

registry = ConnectorRegistry()


# =========================================================
# PUBLIC API
# =========================================================

__all__ = [
    "ConnectorRegistry",
    "registry",
]
