"""
MAIN BASE FOUNDATION

SUPREME — Creator Platform Connector

Provider-neutral connector contract for authorized
creator/content platforms.
"""

from __future__ import annotations

from typing import List, Optional

from ..base import (
    ConnectorCapability,
    ConnectorResult,
    EcosystemProviderConnector,
)

from .capabilities import (
    ProviderCapability,
)


class CreatorPlatformConnector(
    EcosystemProviderConnector
):
    """Base connector for an authorized creator platform."""

    provider_name = "CREATOR_PLATFORM"

    provider_version = "1.0"

    # =====================================================
    # 🆔 PROVIDER INFORMATION
    # =====================================================

    def provider_id(self) -> str:
        """Return the stable provider identifier."""

        return "creator_platform"

    # =====================================================
    # ❤️ HEALTH CHECK
    # =====================================================

    def health_check(self) -> ConnectorResult:
        """Return safe connector health status."""

        return ConnectorResult(
            success=True,
            operation="HEALTH_CHECK",
            provider=self.provider_id(),
            message=(
                "Creator platform connector is operational."
            ),
        )

    # =====================================================
    # 🔐 AUTHORIZATION
    # =====================================================

    def authorization_url(
        self,
        state: str,
    ) -> Optional[str]:
        """
        Return an authorization URL when a real provider
        implementation supplies one.

        The base creator-platform connector does not
        provide a provider-specific URL.
        """

        if not state.strip():
            raise ValueError(
                "state cannot be empty."
            )

        return None

    # =====================================================
    # 🔗 CONNECTION
    # =====================================================

    def connect(
        self,
        authorization_reference: str,
    ) -> ConnectorResult:
        """
        Establish an authorized creator-platform
        connection reference.
        """

        if not authorization_reference.strip():
            return ConnectorResult(
                success=False,
                operation="CONNECT",
                provider=self.provider_id(),
                message=(
                    "Authorization reference is required."
                ),
                error_code="AUTHORIZATION_REQUIRED",
            )

        return ConnectorResult(
            success=True,
            operation="CONNECT",
            provider=self.provider_id(),
            message=(
                "Authorized creator-platform "
                "connection accepted."
            ),
            data={
                "provider_capability": (
                    ProviderCapability.ACCOUNT.value
                ),
            },
        )

    # =====================================================
    # 🔌 DISCONNECTION
    # =====================================================

    def disconnect(
        self,
        connection_reference: str,
    ) -> ConnectorResult:
        """Disconnect an authorized account connection."""

        if not connection_reference.strip():
            return ConnectorResult(
                success=False,
                operation="DISCONNECT",
                provider=self.provider_id(),
                message=(
                    "Connection reference is required."
                ),
                error_code="CONNECTION_REQUIRED",
            )

        return ConnectorResult(
            success=True,
            operation="DISCONNECT",
            provider=self.provider_id(),
            message=(
                "Creator-platform connection "
                "disconnected."
            ),
        )

    # =====================================================
    # 📋 CAPABILITIES
    # =====================================================

    def capabilities(
        self,
    ) -> List[ConnectorCapability]:
        """
        Return generic creator-platform capabilities.

        Actual availability must be determined by the
        specific provider's official authorization/API.
        """

        return [
            ConnectorCapability(
                name=ProviderCapability.ACCOUNT.value,
                description=(
                    "Access provider account information "
                    "where officially supported."
                ),
                requires_authorization=True,
            ),

            ConnectorCapability(
                name=ProviderCapability.CONTENT.value,
                description=(
                    "Access creator content where "
                    "officially supported."
                ),
                requires_authorization=True,
            ),

            ConnectorCapability(
                name=(
                    ProviderCapability.CONTENT_MANAGEMENT.value
                ),
                description=(
                    "Manage creator content where "
                    "officially supported."
                ),
                requires_authorization=True,
            ),

            ConnectorCapability(
                name=ProviderCapability.PUBLISHING.value,
                description=(
                    "Publish content where the provider "
                    "officially supports publishing."
                ),
                requires_authorization=True,
            ),

            ConnectorCapability(
                name=ProviderCapability.ANALYTICS.value,
                description=(
                    "Access creator analytics where "
                    "officially supported."
                ),
                requires_authorization=True,
            ),

            ConnectorCapability(
                name=ProviderCapability.REVENUE.value,
                description=(
                    "Access revenue information where "
                    "officially supported."
                ),
                requires_authorization=True,
            ),

            ConnectorCapability(
                name=ProviderCapability.AFFILIATE.value,
                description=(
                    "Access affiliate functionality where "
                    "officially supported."
                ),
                requires_authorization=True,
            ),

            ConnectorCapability(
                name=ProviderCapability.WEBHOOK.value,
                description=(
                    "Receive provider events through "
                    "officially supported webhooks."
                ),
                requires_authorization=True,
            ),
        ]


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "CreatorPlatformConnector",
]
