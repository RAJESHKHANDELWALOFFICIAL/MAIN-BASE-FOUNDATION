"""
MAIN BASE FOUNDATION

SUPREME — Provider Connector Registration
"""

from __future__ import annotations

from typing import Iterable, Type

from ..base import EcosystemProviderConnector
from ..registry import ConnectorRegistry

from .creator_platform import (
    CreatorPlatformConnector,
)


# =========================================================
# 🧩 BUILT-IN CONNECTORS
# =========================================================

BUILT_IN_CONNECTORS = (
    CreatorPlatformConnector,
)


# =========================================================
# 🔌 REGISTER ONE
# =========================================================

def register_connector(
    registry: ConnectorRegistry,
    connector_class: Type[
        EcosystemProviderConnector
    ],
) -> ConnectorRegistry:
    """Register one provider connector."""

    registry.register(
        connector_class
    )

    return registry


# =========================================================
# 🔌 REGISTER MANY
# =========================================================

def register_connectors(
    registry: ConnectorRegistry,
    connector_classes: Iterable[
        Type[EcosystemProviderConnector]
    ],
) -> ConnectorRegistry:
    """Register multiple provider connectors."""

    for connector_class in connector_classes:
        registry.register(
            connector_class
        )

    return registry


# =========================================================
# 🚀 REGISTER BUILT-INS
# =========================================================

def register_builtin_connectors(
    registry: ConnectorRegistry,
) -> ConnectorRegistry:
    """
    Register SUPREME built-in connector implementations.
    """

    return register_connectors(
        registry=registry,
        connector_classes=BUILT_IN_CONNECTORS,
    )


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "BUILT_IN_CONNECTORS",
    "register_connector",
    "register_connectors",
    "register_builtin_connectors",
]
