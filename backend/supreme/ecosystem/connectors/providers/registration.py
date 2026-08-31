"""
MAIN BASE FOUNDATION

SUPREME — Provider Connector Registration

Central registration entry point for provider connectors.

This module:
- Keeps provider registration centralized.
- Does not store credentials.
- Does not authenticate external accounts.
- Does not invent unsupported provider APIs.
"""

from __future__ import annotations

from typing import Iterable, Type

from ..base import EcosystemProviderConnector
from ..registry import ConnectorRegistry


def register_connectors(
    registry: ConnectorRegistry,
    connector_classes: Iterable[
        Type[EcosystemProviderConnector]
    ],
) -> ConnectorRegistry:
    """
    Register a collection of provider connector classes.

    Provider implementations must explicitly be supplied.
    """

    for connector_class in connector_classes:
        registry.register(connector_class)

    return registry


def register_connector(
    registry: ConnectorRegistry,
    connector_class: Type[
        EcosystemProviderConnector
    ],
) -> ConnectorRegistry:
    """
    Register one provider connector.
    """

    registry.register(connector_class)

    return registry


__all__ = [
    "register_connectors",
    "register_connector",
]
