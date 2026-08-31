"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Provider Connector Base

Common abstract contract for all external platform connectors.

Supported connector categories may include:
- Social platforms
- Creator platforms
- Content platforms
- Professional platforms
- Cloud platforms
- Generic APIs
- Other authorized external providers

Security principles:
- Never store plaintext passwords.
- Never store OTPs.
- Never expose access tokens or API secrets.
- Authentication remains with the external provider.
- Connector code only operates on authorized provider access.
- Provider-specific implementations belong outside this base class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# =========================================================
# 🕐 TIME
# =========================================================


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(
        timezone.utc
    ).isoformat()


# =========================================================
# 🔌 CONNECTOR RESULT
# =========================================================


@dataclass
class ConnectorResult:
    """
    Standard result returned by connector operations.

    Raw credentials and secrets must never be included.
    """

    success: bool

    operation: str

    provider: str

    message: str = ""

    data: Dict[str, Any] = field(
        default_factory=dict
    )

    error_code: Optional[str] = None

    created_at: str = field(
        default_factory=utc_now
    )


# =========================================================
# 🔐 CONNECTOR CAPABILITY
# =========================================================


@dataclass(frozen=True)
class ConnectorCapability:
    """
    Describes one operation supported by a provider connector.
    """

    name: str

    description: str

    requires_authorization: bool = True

    scopes: List[str] = field(
        default_factory=list
    )


# =========================================================
# 🌐 PROVIDER CONNECTOR
# =========================================================


class EcosystemProviderConnector(ABC):
    """
    Abstract base class for all SUPREME ecosystem
    provider connectors.

    Provider implementations must inherit from this class.
    """

    provider_name: str = "GENERIC"

    provider_version: str = "1.0"

    # =====================================================
    # 🆔 PROVIDER INFORMATION
    # =====================================================

    @abstractmethod
    def provider_id(self) -> str:
        """
        Return the stable provider identifier.
        """
        raise NotImplementedError

    # =====================================================
    # ❤️ HEALTH CHECK
    # =====================================================

    @abstractmethod
    def health_check(self) -> ConnectorResult:
        """
        Check whether the connector is operational.

        This must not expose credentials or secrets.
        """
        raise NotImplementedError

    # =====================================================
    # 🔐 AUTHORIZATION
    # =====================================================

    @abstractmethod
    def authorization_url(
        self,
        state: str,
    ) -> Optional[str]:
        """
        Return an external authorization URL when
        the provider supports an authorization flow.

        The provider handles authentication directly.
        """
        raise NotImplementedError

    # =====================================================
    # 🔗 CONNECTION
    # =====================================================

    @abstractmethod
    def connect(
        self,
        authorization_reference: str,
    ) -> ConnectorResult:
        """
        Establish a connection using an already-authorized
        provider authorization reference.

        Raw passwords, OTPs and secrets are not accepted.
        """
        raise NotImplementedError

    # =====================================================
    # 🔌 DISCONNECTION
    # =====================================================

    @abstractmethod
    def disconnect(
        self,
        connection_reference: str,
    ) -> ConnectorResult:
        """
        Disconnect an existing provider connection.
        """
        raise NotImplementedError

    # =====================================================
    # 📋 CAPABILITIES
    # =====================================================

    @abstractmethod
    def capabilities(
        self,
    ) -> List[ConnectorCapability]:
        """
        Return supported provider capabilities.
        """
        raise NotImplementedError

    # =====================================================
    # 📊 STATUS
    # =====================================================

    def status(self) -> Dict[str, Any]:
        """
        Return safe connector status information.

        No secrets are returned.
        """

        return {
            "provider": self.provider_id(),
            "provider_name": self.provider_name,
            "provider_version": self.provider_version,
            "connector": self.__class__.__name__,
            "capabilities": [
                capability.name
                for capability
                in self.capabilities()
            ],
        }


# =========================================================
# 📦 PUBLIC API
# =========================================================


__all__ = [
    "ConnectorResult",
    "ConnectorCapability",
    "EcosystemProviderConnector",
]
