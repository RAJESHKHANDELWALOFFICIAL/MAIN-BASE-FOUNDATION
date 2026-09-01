"""
MAIN BASE FOUNDATION

SUPREME — Provider Capability Definitions

Standard capability identifiers for authorized
creator, content, affiliate and external providers.

This module defines capability names only.
Actual availability depends on the provider's
official authorization/API support.
"""

from __future__ import annotations

from enum import Enum


# =========================================================
# 🔌 PROVIDER CAPABILITIES
# =========================================================


class ProviderCapability(str, Enum):
    """Standard provider capability identifiers."""

    ACCOUNT = "ACCOUNT"

    CONTENT = "CONTENT"

    CONTENT_MANAGEMENT = "CONTENT_MANAGEMENT"

    PUBLISHING = "PUBLISHING"

    ANALYTICS = "ANALYTICS"

    REVENUE = "REVENUE"

    AFFILIATE = "AFFILIATE"

    WEBHOOK = "WEBHOOK"


# =========================================================
# 🔐 AUTHORIZATION REQUIREMENT
# =========================================================


class CapabilityAuthorization(str, Enum):
    """Authorization requirements for capabilities."""

    NONE = "NONE"

    ACCOUNT_AUTHORIZATION = (
        "ACCOUNT_AUTHORIZATION"
    )

    PROVIDER_APPROVAL = (
        "PROVIDER_APPROVAL"
    )


# =========================================================
# 📦 PUBLIC API
# =========================================================


__all__ = [
    "ProviderCapability",
    "CapabilityAuthorization",
]
