"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Connector Public Interface

Central public interface for provider connectors.
"""

from .base import (
    EcosystemProviderConnector,
)

from .registry import (
    ConnectorRegistry,
)


__all__ = [
    "EcosystemProviderConnector",
    "ConnectorRegistry",
]
