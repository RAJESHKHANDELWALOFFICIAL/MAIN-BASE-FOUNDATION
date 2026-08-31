"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Provider Catalog

Central non-secret metadata for external providers.

Important:
- This catalog does not authenticate accounts.
- This catalog does not store credentials.
- This catalog does not claim unsupported APIs.
- Actual capabilities must be verified against the
  provider's official integration documentation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


# =========================================================
# 🌐 PROVIDER CATEGORY
# =========================================================


class ProviderCategory(str, Enum):
    """High-level external provider categories."""

    IDENTITY = "IDENTITY"
    CLOUD = "CLOUD"
    HOSTING = "HOSTING"
    SOCIAL = "SOCIAL"
    CREATOR = "CREATOR"
    CONTENT = "CONTENT"
    PROFESSIONAL = "PROFESSIONAL"
    GENERIC = "GENERIC"


# =========================================================
# 🔌 AUTHORIZATION TYPE
# =========================================================


class ProviderAuthorizationType(str, Enum):
    """Supported authorization mechanisms."""

    OAUTH = "OAUTH"
    API_KEY = "API_KEY"
    ACCESS_TOKEN = "ACCESS_TOKEN"
    IAM = "IAM"
    MANUAL = "MANUAL"
    UNKNOWN = "UNKNOWN"


# =========================================================
# 📋 PROVIDER DEFINITION
# =========================================================


@dataclass(frozen=True)
class ProviderDefinition:
    """
    Non-secret provider definition.

    No credentials or private account information belongs here.
    """

    provider_id: str

    display_name: str

    category: ProviderCategory

    authorization_type: ProviderAuthorizationType = (
        ProviderAuthorizationType.UNKNOWN
    )

    official_domain: str = ""

    capabilities: List[str] = field(
        default_factory=list
    )

    enabled: bool = True

    verified: bool = False

    notes: str = ""


# =========================================================
# 🌍 CORE PROVIDER CATALOG
# =========================================================


PROVIDER_CATALOG: List[ProviderDefinition] = [
    ProviderDefinition(
        provider_id="google",
        display_name="Google",
        category=ProviderCategory.IDENTITY,
        authorization_type=(
            ProviderAuthorizationType.OAUTH
        ),
        official_domain="google.com",
    ),

    ProviderDefinition(
        provider_id="microsoft",
        display_name="Microsoft",
        category=ProviderCategory.IDENTITY,
        authorization_type=(
            ProviderAuthorizationType.OAUTH
        ),
        official_domain="microsoft.com",
    ),

    ProviderDefinition(
        provider_id="aws",
        display_name="AWS",
        category=ProviderCategory.CLOUD,
        authorization_type=(
            ProviderAuthorizationType.IAM
        ),
        official_domain="aws.amazon.com",
    ),

    ProviderDefinition(
        provider_id="apple",
        display_name="Apple",
        category=ProviderCategory.IDENTITY,
        authorization_type=(
            ProviderAuthorizationType.OAUTH
        ),
        official_domain="apple.com",
    ),
]


# =========================================================
# 🔎 LOOKUP
# =========================================================


def get_provider(
    provider_id: str,
) -> ProviderDefinition | None:
    """Return a provider definition by identifier."""

    normalized_id = provider_id.strip().lower()

    for provider in PROVIDER_CATALOG:
        if provider.provider_id == normalized_id:
            return provider

    return None


# =========================================================
# 📋 LIST
# =========================================================


def list_providers() -> List[ProviderDefinition]:
    """Return all catalogued providers."""

    return list(PROVIDER_CATALOG)


# =========================================================
# 📦 PUBLIC API
# =========================================================


__all__ = [
    "ProviderCategory",
    "ProviderAuthorizationType",
    "ProviderDefinition",
    "PROVIDER_CATALOG",
    "get_provider",
    "list_providers",
]
