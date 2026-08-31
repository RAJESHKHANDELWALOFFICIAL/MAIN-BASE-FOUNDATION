"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Provider Connectors

Public interface for:
- Provider catalog
- Provider definitions
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

from .registration import (
    register_connector,
    register_connectors,
)


__all__ = [
    # Provider Catalog
    "ProviderCategory",
    "ProviderAuthorizationType",
    "ProviderDefinition",
    "PROVIDER_CATALOG",
    "get_provider",
    "list_providers",

    # Registration
    "register_connector",
    "register_connectors",
]
