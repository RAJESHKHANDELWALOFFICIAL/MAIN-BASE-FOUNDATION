"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Integration Models

Central integration models for external providers.

Integration ownership:

SUPREME ECOSYSTEM
        ↓
VAULT
        ↓
INTEGRATION
        ↓
EXTERNAL PROVIDER ACCOUNT

Security principles:
- Never store plaintext passwords.
- Never store OTPs.
- Never expose raw secrets.
- Store only secure credential references.
- Provider authorization remains with the external provider.
- Every integration belongs to a specific vault.
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

    return datetime.now(
        timezone.utc
    ).isoformat()


# =========================================================
# 🌐 PROVIDER
# =========================================================


class IntegrationProvider(str, Enum):
    """Supported external integration providers."""

    GOOGLE = "GOOGLE"
    MICROSOFT = "MICROSOFT"
    AWS = "AWS"
    APPLE = "APPLE"

    GENERIC_WEB = "GENERIC_WEB"

    CREATOR_PLATFORM = "CREATOR_PLATFORM"


# =========================================================
# 🔌 INTEGRATION TYPE
# =========================================================


class IntegrationType(str, Enum):
    """Supported integration connection types."""

    OAUTH = "OAUTH"
    API = "API"
    CLOUD = "CLOUD"
    IAM = "IAM"
    WEBHOOK = "WEBHOOK"
    MANUAL = "MANUAL"
    OTHER = "OTHER"


# =========================================================
# 📊 CONNECTION STATUS
# =========================================================


class IntegrationStatus(str, Enum):
    """Integration lifecycle status."""

    PENDING = "PENDING"

    AUTHORIZED = "AUTHORIZED"

    CONNECTED = "CONNECTED"

    EXPIRED = "EXPIRED"

    REVOKED = "REVOKED"

    SUSPENDED = "SUSPENDED"

    DISCONNECTED = "DISCONNECTED"

    ERROR = "ERROR"


# =========================================================
# 🔐 CREDENTIAL REFERENCE
# =========================================================


@dataclass
class IntegrationCredentialReference:
    """
    Secure reference to credentials stored by the vault.

    The actual password, token, API key or secret is NOT
    stored in this model.
    """

    credential_reference_id: str

    vault_id: str

    credential_type: str

    encrypted_secret_reference: Optional[str] = None

    key_version: str = "1.0"

    active: bool = True

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.credential_reference_id.strip():
            raise ValueError(
                "credential_reference_id cannot be empty."
            )

        if not self.vault_id.strip():
            raise ValueError(
                "vault_id cannot be empty."
            )

        if not self.credential_type.strip():
            raise ValueError(
                "credential_type cannot be empty."
            )


# =========================================================
# 🔗 INTEGRATION CONNECTION
# =========================================================


@dataclass
class EcosystemIntegration:
    """
    External provider connection belonging to a SUPREME
    ecosystem vault.
    """

    integration_id: str

    vault_id: str

    owner_id: str

    provider: IntegrationProvider

    integration_type: IntegrationType

    account_reference: str = ""

    display_name: str = ""

    status: IntegrationStatus = (
        IntegrationStatus.PENDING
    )

    credential_reference_id: Optional[str] = None

    scopes: List[str] = field(
        default_factory=list
    )

    capabilities: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    active: bool = True

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    last_connected_at: Optional[str] = None

    last_error: Optional[str] = None

    def __post_init__(self) -> None:

        if not self.integration_id.strip():
            raise ValueError(
                "integration_id cannot be empty."
            )

        if not self.vault_id.strip():
            raise ValueError(
                "vault_id cannot be empty."
            )

        if not self.owner_id.strip():
            raise ValueError(
                "owner_id cannot be empty."
            )

        if not self.display_name.strip():
            self.display_name = (
                f"{self.provider.value} "
                f"Integration"
            )


# =========================================================
# 🔑 AUTHORIZATION SCOPE
# =========================================================


@dataclass
class IntegrationAuthorization:
    """
    Authorization granted to an integration.

    Scopes define what the external provider connection
    is allowed to access.
    """

    integration_id: str

    authorized_by: str

    scopes: List[str] = field(
        default_factory=list
    )

    granted: bool = False

    authorization_reference: Optional[str] = None

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

        if not self.authorized_by.strip():
            raise ValueError(
                "authorized_by cannot be empty."
            )


# =========================================================
# 🛡️ INTEGRATION ACCESS DECISION
# =========================================================


@dataclass(frozen=True)
class IntegrationAccessDecision:
    """Result of an integration access check."""

    integration_id: str

    user_id: str

    allowed: bool

    action: str

    reason: str = ""

    checked_at: str = field(
        default_factory=utc_now
    )


# =========================================================
# 📦 PUBLIC API
# =========================================================


__all__ = [
    "IntegrationProvider",
    "IntegrationType",
    "IntegrationStatus",
    "IntegrationCredentialReference",
    "EcosystemIntegration",
    "IntegrationAuthorization",
    "IntegrationAccessDecision",
]
