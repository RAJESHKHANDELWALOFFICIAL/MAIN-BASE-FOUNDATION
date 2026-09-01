"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Integration Service

Central service for managing:

- Provider integrations
- Integration authorization
- Integration status
- Integration lifecycle
- Vault association
- Access verification
- Provider connector access

Security principles:
- Every integration belongs to a vault.
- Raw passwords are never stored.
- Raw secrets are never returned.
- Credentials are represented by secure references.
- Provider-specific authentication remains outside this service.
- Provider connectors operate only through authorized access.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

from backend.supreme.ecosystem.integration.model import (
    EcosystemIntegration,
    IntegrationAccessDecision,
    IntegrationAuthorization,
    IntegrationCredentialReference,
    IntegrationProvider,
    IntegrationStatus,
    IntegrationType,
)

from backend.supreme.ecosystem.vault.service import (
    VaultService,
)

from backend.supreme.ecosystem.connectors.manager import (
    ConnectorManager,
    connector_manager as default_connector_manager,
)


class IntegrationService:
    """Central SUPREME ecosystem integration service."""

    def __init__(
        self,
        vault_service: Optional[VaultService] = None,
        connector_manager: Optional[
            ConnectorManager
        ] = None,
    ) -> None:

        self.vault_service = (
            vault_service
            if vault_service is not None
            else VaultService()
        )

        self.connector_manager = (
            connector_manager
            if connector_manager is not None
            else default_connector_manager
        )

        self._integrations: Dict[
            str,
            EcosystemIntegration,
        ] = {}

        self._credentials: Dict[
            str,
            IntegrationCredentialReference,
        ] = {}

        self._authorizations: Dict[
            str,
            IntegrationAuthorization,
        ] = {}

        self._initialized = False

    # =========================================================
    # 🚀 INITIALIZE
    # =========================================================

    def initialize(self) -> dict:
        """Initialize the integration service."""

        self.vault_service.initialize()
        self.connector_manager.initialize()

        self._initialized = True

        return {
            "service": "SUPREME_ECOSYSTEM_INTEGRATION",
            "status": "READY",
            "initialized": True,
            "connector_manager": (
                self.connector_manager.status()
            ),
        }

    # =========================================================
    # 🔌 CREATE INTEGRATION
    # =========================================================

    def create_integration(
        self,
        integration: EcosystemIntegration,
        requested_by: str,
    ) -> EcosystemIntegration:
        """
        Create a provider integration record.

        The integration is initially PENDING until the
        external provider authorization succeeds.
        """

        if (
            integration.integration_id
            in self._integrations
        ):
            raise ValueError(
                "Integration already exists."
            )

        vault = self.vault_service.get_vault(
            integration.vault_id
        )

        if vault is None:
            raise ValueError(
                "Integration vault does not exist."
            )

        decision = self._check_vault_access(
            vault_id=integration.vault_id,
            user_id=requested_by,
            action="MANAGE_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        if (
            integration.owner_id
            != vault.owner_id
        ):
            raise ValueError(
                "Integration owner does not match vault owner."
            )

        self._integrations[
            integration.integration_id
        ] = integration

        return integration

    # =========================================================
    # 🔎 GET INTEGRATION
    # =========================================================

    def get_integration(
        self,
        integration_id: str,
        requested_by: str,
    ) -> Optional[EcosystemIntegration]:
        """Return an authorized integration."""

        integration = self._integrations.get(
            integration_id
        )

        if integration is None:
            return None

        decision = self._check_vault_access(
            vault_id=integration.vault_id,
            user_id=requested_by,
            action="READ_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        return integration

    # =========================================================
    # 📋 LIST INTEGRATIONS
    # =========================================================

    def list_integrations(
        self,
        vault_id: str,
        requested_by: str,
    ) -> List[EcosystemIntegration]:
        """List integrations belonging to a vault."""

        self._require_vault(
            vault_id
        )

        decision = self._check_vault_access(
            vault_id=vault_id,
            user_id=requested_by,
            action="READ_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        return [
            integration
            for integration
            in self._integrations.values()
            if integration.vault_id == vault_id
            and integration.active
        ]

    # =========================================================
    # 🔐 REGISTER CREDENTIAL REFERENCE
    # =========================================================

    def register_credential_reference(
        self,
        reference: IntegrationCredentialReference,
        requested_by: str,
    ) -> IntegrationCredentialReference:
        """
        Register a secure credential reference.

        No plaintext credential is accepted here.
        """

        self._require_vault(
            reference.vault_id
        )

        decision = self._check_vault_access(
            vault_id=reference.vault_id,
            user_id=requested_by,
            action="MANAGE_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        if (
            reference.credential_reference_id
            in self._credentials
        ):
            raise ValueError(
                "Credential reference already exists."
            )

        self._credentials[
            reference.credential_reference_id
        ] = reference

        return reference

    # =========================================================
    # 🔗 ATTACH CREDENTIAL
    # =========================================================

    def attach_credential(
        self,
        integration_id: str,
        credential_reference_id: str,
        requested_by: str,
    ) -> EcosystemIntegration:
        """Attach a secure credential reference."""

        integration = self._require_integration(
            integration_id
        )

        credential = self._credentials.get(
            credential_reference_id
        )

        if credential is None:
            raise ValueError(
                "Credential reference does not exist."
            )

        if (
            credential.vault_id
            != integration.vault_id
        ):
            raise PermissionError(
                "Credential and integration belong to different vaults."
            )

        decision = self._check_vault_access(
            vault_id=integration.vault_id,
            user_id=requested_by,
            action="MANAGE_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        integration.credential_reference_id = (
            credential_reference_id
        )

        integration.updated_at = (
            self._now()
        )

        return integration

    # =========================================================
    # 🔐 AUTHORIZE
    # =========================================================

    def authorize(
        self,
        integration_id: str,
        authorized_by: str,
        scopes: Optional[List[str]] = None,
        authorization_reference: Optional[str] = None,
    ) -> IntegrationAuthorization:
        """
        Record provider authorization.

        Actual provider authentication is performed by the
        provider-specific connector.
        """

        integration = self._require_integration(
            integration_id
        )

        decision = self._check_vault_access(
            vault_id=integration.vault_id,
            user_id=authorized_by,
            action="MANAGE_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        authorization = IntegrationAuthorization(
            integration_id=integration_id,
            authorized_by=authorized_by,
            scopes=list(scopes or []),
            granted=True,
            authorization_reference=(
                authorization_reference
            ),
        )

        self._authorizations[
            integration_id
        ] = authorization

        integration.scopes = list(
            authorization.scopes
        )

        integration.status = (
            IntegrationStatus.AUTHORIZED
        )

        integration.updated_at = (
            self._now()
        )

        return authorization

    # =========================================================
    # 🔗 CONNECT
    # =========================================================

    def mark_connected(
        self,
        integration_id: str,
        requested_by: str,
    ) -> EcosystemIntegration:
        """
        Mark an already-authorized integration as connected.

        The actual provider connection is handled by
        the provider-specific connector.
        """

        integration = self._require_integration(
            integration_id
        )

        decision = self._check_vault_access(
            vault_id=integration.vault_id,
            user_id=requested_by,
            action="MANAGE_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        authorization = self._authorizations.get(
            integration_id
        )

        if (
            authorization is None
            or not authorization.granted
        ):
            raise PermissionError(
                "Integration has not been authorized."
            )

        integration.status = (
            IntegrationStatus.CONNECTED
        )

        integration.last_connected_at = (
            self._now()
        )

        integration.updated_at = (
            self._now()
        )

        integration.last_error = None

        return integration

    # =========================================================
    # 🔌 DISCONNECT
    # =========================================================

    def disconnect(
        self,
        integration_id: str,
        requested_by: str,
    ) -> EcosystemIntegration:
        """Disconnect an integration."""

        integration = self._require_integration(
            integration_id
        )

        decision = self._check_vault_access(
            vault_id=integration.vault_id,
            user_id=requested_by,
            action="MANAGE_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        integration.status = (
            IntegrationStatus.DISCONNECTED
        )

        integration.active = False

        integration.updated_at = (
            self._now()
        )

        return integration

    # =========================================================
    # 🚫 REVOKE AUTHORIZATION
    # =========================================================

    def revoke_authorization(
        self,
        integration_id: str,
        requested_by: str,
    ) -> EcosystemIntegration:
        """Revoke an integration authorization."""

        integration = self._require_integration(
            integration_id
        )

        decision = self._check_vault_access(
            vault_id=integration.vault_id,
            user_id=requested_by,
            action="MANAGE_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        authorization = self._authorizations.get(
            integration_id
        )

        if authorization is not None:
            authorization.granted = False
            authorization.updated_at = (
                self._now()
            )

        integration.status = (
            IntegrationStatus.REVOKED
        )

        integration.active = False

        integration.updated_at = (
            self._now()
        )

        return integration

    # =========================================================
    # 🛡️ ACCESS CHECK
    # =========================================================

    def check_access(
        self,
        integration_id: str,
        user_id: str,
        action: str,
    ) -> IntegrationAccessDecision:
        """Check integration access through its vault."""

        integration = self._integrations.get(
            integration_id
        )

        if integration is None:
            return IntegrationAccessDecision(
                integration_id=integration_id,
                user_id=user_id,
                allowed=False,
                action=action,
                reason="Integration does not exist.",
            )

        decision = self._check_vault_access(
            vault_id=integration.vault_id,
            user_id=user_id,
            action=action,
        )

        return IntegrationAccessDecision(
            integration_id=integration_id,
            user_id=user_id,
            allowed=decision.allowed,
            action=action,
            reason=decision.reason,
        )

    # =========================================================
    # 🔎 PROVIDER FILTER
    # =========================================================

    def list_by_provider(
        self,
        provider: IntegrationProvider,
        requested_by: str,
    ) -> List[EcosystemIntegration]:
        """List integrations for a provider."""

        results: List[EcosystemIntegration] = []

        for integration in self._integrations.values():

            if integration.provider != provider:
                continue

            decision = self._check_vault_access(
                vault_id=integration.vault_id,
                user_id=requested_by,
                action="READ_INTEGRATION",
            )

            if (
                decision.allowed
                and integration.active
            ):
                results.append(
                    integration
                )

        return results

    # =========================================================
    # 🔌 CONNECTOR ACCESS
    # =========================================================

    def get_connector(
        self,
        provider_id: str,
    ) -> Optional[
        EcosystemProviderConnector
    ]:
        """
        Return a registered provider connector.

        No credentials are exposed.
        """

        return self.connector_manager.get_connector(
            provider_id
        )

    def list_connector_providers(
        self,
    ) -> List[str]:
        """Return registered connector providers."""

        return self.connector_manager.providers()

    def connector_status(
        self,
    ) -> Dict[str, Any]:
        """Return safe connector manager status."""

        return self.connector_manager.status()

    def connector_health_check(
        self,
        provider_id: str,
    ) -> ConnectorResult:
        """Run a safe connector health check."""

        return self.connector_manager.health_check(
            provider_id
        )

    # =========================================================
    # 🔎 INTERNAL HELPERS
    # =========================================================

    def _require_integration(
        self,
        integration_id: str,
    ) -> EcosystemIntegration:
        """Return an existing integration."""

        integration = self._integrations.get(
            integration_id
        )

        if integration is None:
            raise ValueError(
                "Integration does not exist."
            )

        return integration

    def _require_vault(
        self,
        vault_id: str,
    ):
        """Return an existing vault."""

        vault = self.vault_service.get_vault(
            vault_id
        )

        if vault is None:
            raise ValueError(
                "Vault does not exist."
            )

        return vault

    def _check_vault_access(
        self,
        vault_id: str,
        user_id: str,
        action: str,
    ):
        """Delegate access control to VaultService."""

        return self.vault_service.check_access(
            vault_id=vault_id,
            user_id=user_id,
            action=action,
        )

    @staticmethod
    def _now() -> str:
        """Return current UTC timestamp."""

        return datetime.now(
            timezone.utc
        ).isoformat()

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return integration service status."""

        return {
            "service": (
                "SUPREME_ECOSYSTEM_INTEGRATION"
            ),
            "initialized": self._initialized,
            "integrations": len(
                self._integrations
            ),
            "credentials": len(
                self._credentials
            ),
            "authorizations": len(
                self._authorizations
            ),
            "providers": [
                provider.value
                for provider
                in IntegrationProvider
            ],
            "connector_manager": (
                self.connector_manager.status()
            ),
        }


__all__ = [
    "IntegrationService",
]
