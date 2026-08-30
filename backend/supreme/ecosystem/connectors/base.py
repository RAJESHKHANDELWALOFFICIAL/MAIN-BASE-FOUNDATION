"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Provider Connector Contract

Common interface for external platform connectors.

The connector layer is responsible for:
- Provider identification
- Initialization
- Authorization handoff
- Connection lifecycle
- Disconnection
- Health/status reporting

Security principles:
- No plaintext passwords
- No OTP storage
- No raw credentials in connector objects
- Credentials are handled through secure references
- Provider-specific authentication remains provider-controlled
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from backend.supreme.ecosystem.integration.model import (
    IntegrationProvider,
)


class EcosystemProviderConnector(ABC):
    """
    Abstract connector contract for external providers.

    Concrete providers implement this contract without changing
    the central IntegrationService architecture.
    """

    def __init__(
        self,
        provider: IntegrationProvider,
    ) -> None:

        self.provider = provider
        self._initialized = False

    # =========================================================
    # 🚀 INITIALIZE
    # =========================================================

    @abstractmethod
    def initialize(self) -> dict:
        """
        Initialize the provider connector.
        """

        raise NotImplementedError

    # =========================================================
    # 🌐 PROVIDER
    # =========================================================

    def provider_name(self) -> str:
        """
        Return the provider name.
        """

        return self.provider.value

    # =========================================================
    # 🔐 AUTHORIZATION
    # =========================================================

    @abstractmethod
    def authorization_url(
        self,
        state: str,
        redirect_uri: str,
    ) -> Optional[str]:
        """
        Return a provider authorization URL when supported.

        Providers that do not expose a supported authorization
        URL may return None.
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
        Establish a provider connection using an already
        authorized provider reference.

        Raw credentials must not be passed into this method.
        """

        raise NotImplementedError

    # =========================================================
    # 🔌 DISCONNECT
    # =========================================================

    @abstractmethod
    def disconnect(
        self,
        connection_reference: str,
    ) -> bool:
        """
        Disconnect an existing provider connection.
        """

        raise NotImplementedError

    # =========================================================
    # ❤️ HEALTH
    # =========================================================

    @abstractmethod
    def health(
        self,
        connection_reference: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Return provider connector health information.
        """

        raise NotImplementedError

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """
        Return connector status.
        """

        return {
            "connector": self.__class__.__name__,
            "provider": self.provider.value,
            "initialized": self._initialized,
        }


__all__ = [
    "EcosystemProviderConnector",
]
