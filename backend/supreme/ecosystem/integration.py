"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Integration Control

Central integration-control model connecting:

SUPREME
    ↓
ECOSYSTEM
    ↓
ENTITY
    ↓
OWNERSHIP
    ↓
EXTERNAL INTEGRATION

The external provider remains externally controlled.

SUPREME controls the integration relationship inside
MAIN BASE FOUNDATION through ownership, permissions,
scopes, status and authorization references.

No provider secrets are stored here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional


# =========================================================
# 🕐 TIME
# =========================================================


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


# =========================================================
# 🔌 INTEGRATION STATUS
# =========================================================


class EcosystemIntegrationStatus(str, Enum):
    """Lifecycle status of an ecosystem integration."""

    REGISTERED = "REGISTERED"
    CONFIGURED = "CONFIGURED"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    ERROR = "ERROR"
    DISABLED = "DISABLED"


# =========================================================
# 🎯 INTEGRATION SCOPE
# =========================================================


class EcosystemIntegrationScope(str, Enum):
    """Scope at which an integration is controlled."""

    ECOSYSTEM = "ECOSYSTEM"
    ENTITY = "ENTITY"
    PROFILE = "PROFILE"
    PAGE = "PAGE"
    GROUP = "GROUP"
    CHANNEL = "CHANNEL"
    COMMUNITY = "COMMUNITY"
    BUSINESS = "BUSINESS"
    USER = "USER"


# =========================================================
# 🔐 INTEGRATION PERMISSION
# =========================================================


class EcosystemIntegrationPermission(str, Enum):
    """Permissions available inside SUPREME."""

    VIEW = "VIEW"

    CONNECT = "CONNECT"
    DISCONNECT = "DISCONNECT"

    READ = "READ"
    WRITE = "WRITE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    CONFIGURE = "CONFIGURE"
    MANAGE = "MANAGE"

    MANAGE_SCOPES = "MANAGE_SCOPES"
    MANAGE_CONNECTION = "MANAGE_CONNECTION"

    HEALTH_CHECK = "HEALTH_CHECK"
    EXECUTE = "EXECUTE"


# =========================================================
# 🔗 ECOSYSTEM INTEGRATION
# =========================================================


@dataclass
class EcosystemIntegration:
    """
    Represents an external integration connected to a
    SUPREME ecosystem entity.

    This object does not store external secrets.

    It stores only the relationship and control metadata
    required by MAIN BASE FOUNDATION.
    """

    integration_id: str

    entity_id: str

    provider_id: str

    connector_id: str

    created_by: str

    scope: EcosystemIntegrationScope = (
        EcosystemIntegrationScope.ENTITY
    )

    status: EcosystemIntegrationStatus = (
        EcosystemIntegrationStatus.REGISTERED
    )

    permissions: List[
        EcosystemIntegrationPermission
    ] = field(
        default_factory=list
    )

    external_account_reference: Optional[str] = None

    credential_reference: Optional[str] = None

    authorized: bool = False

    active: bool = True

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.integration_id.strip():
            raise ValueError(
                "integration_id cannot be empty."
            )

        if not self.entity_id.strip():
            raise ValueError(
                "entity_id cannot be empty."
            )

        if not self.provider_id.strip():
            raise ValueError(
                "provider_id cannot be empty."
            )

        if not self.connector_id.strip():
            raise ValueError(
                "connector_id cannot be empty."
            )

        if not self.created_by.strip():
            raise ValueError(
                "created_by cannot be empty."
            )


# =========================================================
# 👑 INTEGRATION CONTROL
# =========================================================


@dataclass
class EcosystemIntegrationControl:
    """
    SUPREME-side control definition for an integration.

    This determines who can manage the integration inside
    the ecosystem and which operations are permitted.
    """

    integration_id: str

    primary_owner_id: str

    owner_ids: List[str] = field(
        default_factory=list
    )

    admin_ids: List[str] = field(
        default_factory=list
    )

    permissions: Dict[
        str,
        List[EcosystemIntegrationPermission],
    ] = field(
        default_factory=dict
    )

    owner_only: bool = True

    active: bool = True

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.integration_id.strip():
            raise ValueError(
                "integration_id cannot be empty."
            )

        if not self.primary_owner_id.strip():
            raise ValueError(
                "primary_owner_id cannot be empty."
            )


# =========================================================
# 🔐 AUTHORIZATION RESULT
# =========================================================


@dataclass(frozen=True)
class IntegrationAccessDecision:
    """Result of an integration access check."""

    integration_id: str

    user_id: str

    permission: EcosystemIntegrationPermission

    allowed: bool

    reason: str = ""

    checked_at: str = field(
        default_factory=utc_now
    )


# =========================================================
# 📊 INTEGRATION STATUS
# =========================================================


@dataclass
class EcosystemIntegrationStatus:
    """
    Runtime status exposed to the SUPREME ecosystem.
    """

    integration_id: str

    provider_id: str

    status: EcosystemIntegrationStatus = (
        EcosystemIntegrationStatus.REGISTERED
    )

    authorized: bool = False

    healthy: bool = False

    active: bool = True

    message: str = ""

    updated_at: str = field(
        default_factory=utc_now
    )


# =========================================================
# 📦 PUBLIC API
# =========================================================


__all__ = [
    "EcosystemIntegrationStatus",
    "EcosystemIntegrationScope",
    "EcosystemIntegrationPermission",
    "EcosystemIntegration",
    "EcosystemIntegrationControl",
    "IntegrationAccessDecision",
]
