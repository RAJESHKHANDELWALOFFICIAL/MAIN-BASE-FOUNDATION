"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Package

Central public interface for the SUPREME ecosystem.
"""

from .connectors.base import (
    ConnectorResult,
    ConnectorCapability,
    EcosystemProviderConnector,
)

from .connectors.registry import (
    ConnectorRegistry,
    registry,
)

from .connectors.manager import (
    ConnectorManager,
    connector_manager,
)


__all__ = [
    # Connector Base
    "ConnectorResult",
    "ConnectorCapability",
    "EcosystemProviderConnector",

    # Connector Registry
    "ConnectorRegistry",
    "registry",

    # Connector Manager
    "ConnectorManager",
    "connector_manager",
]
