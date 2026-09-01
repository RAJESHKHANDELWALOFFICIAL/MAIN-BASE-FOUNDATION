"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Connector Public Interface

Central public interface for:
- Connector results
- Connector capabilities
- Provider connector base
- Connector registry
- Connector manager
"""

from .base import (
    ConnectorResult,
    ConnectorCapability,
    EcosystemProviderConnector,
)

from .registry import (
    ConnectorRegistry,
    registry,
)

from .manager import (
    ConnectorManager,
    connector_manager,
)


__all__ = [
    # Base
    "ConnectorResult",
    "ConnectorCapability",
    "EcosystemProviderConnector",

    # Registry
    "ConnectorRegistry",
    "registry",

    # Manager
    "ConnectorManager",
    "connector_manager",
]
