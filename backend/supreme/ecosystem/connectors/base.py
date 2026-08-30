"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Provider Connector Base

Common connector contract for external platforms.

The connector layer provides a controlled boundary between
the SUPREME ecosystem and external provider platforms.

Design principles:
- Provider-specific implementations remain separate.
- No plaintext passwords are stored here.
- No OTPs are stored here.
- No provider credentials are exposed here.
- Authorization remains controlled by the external provider.
- Provider capabilities are explicit.
- Unsupported operations must fail safely.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class EcosystemProviderConnector(ABC):
    """
    Abstract base connector for an external provider.

    Every provider-specific connector must implement this
    common interface.
    """

    provider_name: str = ""
    provider_key: str = ""

    # =========================================================
    # 🔎 PROVIDER INFORMATION
    # =========================================================

    @abstractmethod
    def provider_info(self) -> Dict[str, Any]:
        """
        Return non-secret provider information.
        """
        raise NotImplementedError

    # =========================================================
    # 🔐 AUTHORIZATION
    # =========================================================

    @abstractmethod
    def authorization_url(
        self,
        state: str,
    ) -> str:
        """
        Return the provider authorization URL.

        The provider remains responsible for authentication
        and authorization.
        """
        raise NotImplementedError

    # =========================================================
    # 🔗 CONNECTION
    # =========================================================

    @abstractmethod
    def connect(
        self,
        authorization_reference: str,
    ) -> Dict[str, Any]:
        """
        Establish an authorized provider connection.

        Raw credentials must never be returned.
        """
        raise NotImplementedError

    # =========================================================
    # 🔌 DISCONNECTION
    # =========================================================

    @abstractmethod
    def disconnect(
        self,
        account_reference: str,
    ) -> Dict[str, Any]:
        """
        Disconnect an external provider account.
        """
        raise NotImplementedError

    # =========================================================
    # 🛡️ CAPABILITIES
    # =========================================================

    @abstractmethod
    def capabilities(self) -> List[str]:
        """
        Return supported provider capabilities.
        """
        raise NotImplementedError

    # =========================================================
    # ❤️ HEALTH
    # =========================================================

    @abstractmethod
    def health(self) -> Dict[str, Any]:
        """
        Return connector/provider health information.
        """
        raise NotImplementedError


__all__ = [
    "EcosystemProviderConnector",
]
