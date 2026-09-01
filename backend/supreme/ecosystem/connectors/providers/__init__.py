"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Provider Connectors

Public interface for:
- Provider catalog
- Provider capabilities
- Provider definitions
- Provider connector implementations
- Provider registration helpers

No credentials or secrets are exposed here.
"""

from .catalog import (
    ProviderCategory,
    ProviderAuthorizationType,
    ProviderDefinition,
    PROVIDER_CATALOG,
    get_provider,
    list_providers,
)

from .capabilities import (
    ProviderCapability,
    CapabilityAuthorization,
)

from .creator_platform import (
    CreatorPlatformConnector,
)

from .registration import (
    BUILT_IN_CONNECTORS,
    register_connector,
    register_connectors,
    register_builtin_connectors,
)


__all__ = [
    # Provider Catalog
    "ProviderCategory",
    "ProviderAuthorizationType",
    "ProviderDefinition",
    "PROVIDER_CATALOG",
    "get_provider",
    "list_providers",

    # Provider Capabilities
    "ProviderCapability",
    "CapabilityAuthorization",

    # Provider Connectors
    "CreatorPlatformConnector",

    # Registration
    "BUILT_IN_CONNECTORS",
    "register_connector",
    "register_connectors",
    "register_builtin_connectors",
]
