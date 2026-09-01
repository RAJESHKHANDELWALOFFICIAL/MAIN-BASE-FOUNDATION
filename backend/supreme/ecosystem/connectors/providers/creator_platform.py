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


class CreatorPlatformConnector(
    EcosystemProviderConnector
):
    """Base connector for an authorized creator platform."""

    provider_name = "CREATOR_PLATFORM"
    provider_version = "1.0"

    def provider_id(self) -> str:
        return "creator_platform"

    def health_check(self) -> ConnectorResult:
        return ConnectorResult(
            success=True,
            operation="HEALTH_CHECK",
            provider=self.provider_id(),
            message="Creator platform connector is operational.",
        )

    def authorization_url(
        self,
        state: str,
    ) -> Optional[str]:
        if not state.strip():
            raise ValueError("state cannot be empty.")

        return None

    def connect(
        self,
        authorization_reference: str,
    ) -> ConnectorResult:
        if not authorization_reference.strip():
            return ConnectorResult(
                success=False,
                operation="CONNECT",
                provider=self.provider_id(),
                message="Authorization reference is required.",
                error_code="AUTHORIZATION_REQUIRED",
            )

        return ConnectorResult(
            success=True,
            operation="CONNECT",
            provider=self.provider_id(),
            message="Authorized creator-platform connection accepted.",
        )

    def disconnect(
        self,
        connection_reference: str,
    ) -> ConnectorResult:
        if not connection_reference.strip():
            return ConnectorResult(
                success=False,
                operation="DISCONNECT",
                provider=self.provider_id(),
                message="Connection reference is required.",
                error_code="CONNECTION_REQUIRED",
            )

        return ConnectorResult(
            success=True,
            operation="DISCONNECT",
            provider=self.provider_id(),
            message="Creator-platform connection disconnected.",
        )

    def capabilities(
        self,
    ) -> List[ConnectorCapability]:
        return [
            ConnectorCapability(
                name="HEALTH_CHECK",
                description="Check connector health.",
                requires_authorization=False,
            ),
            ConnectorCapability(
                name="CONNECT",
                description="Connect an authorized creator account.",
            ),
            ConnectorCapability(
                name="DISCONNECT",
                description="Disconnect an authorized account.",
            ),
            ConnectorCapability(
                name="ACCOUNT_INFO",
                description="Access provider account information where officially supported.",
            ),
            ConnectorCapability(
                name="CONTENT_MANAGEMENT",
                description="Manage creator content where officially supported.",
            ),
            ConnectorCapability(
                name="ANALYTICS",
                description="Access creator analytics where officially supported.",
            ),
            ConnectorCapability(
                name="REVENUE",
                description="Access revenue information where officially supported.",
            ),
        ]


__all__ = [
    "CreatorPlatformConnector",
]
