"""MAIN BASE FOUNDATION permission API."""

from typing import Dict, List, Optional

from backend.engines.permissions import PermissionEngine


class PermissionAPI:
    """API facade for the MAIN BASE FOUNDATION permission engine."""

    def __init__(self):
        self.engine = PermissionEngine()

    def status(self) -> dict:
        """Return permission engine status."""

        return self.engine.status()

    def health(self) -> dict:
        """Return permission engine health."""

        return self.engine.health()

    def configuration(self) -> dict:
        """Return safe permission configuration."""

        return self.engine.configuration()

    def resources(self) -> dict:
        """Return supported permission resources."""

        return self.engine.resource_types()

    def actions(self) -> dict:
        """Return supported permission actions."""

        return self.engine.action_types()

    def scopes(self) -> dict:
        """Return supported permission scopes."""

        return self.engine.scope_types()

    def conditions(self) -> dict:
        """Return supported permission conditions."""

        return self.engine.condition_types()

    def statuses(self) -> dict:
        """Return supported permission lifecycle statuses."""

        return self.engine.status_types()

    def grant(
        self,
        permission_id: str,
        granted_to: str,
        resource: str,
        action: str,
        scope: str,
        granted_by: Optional[str] = None,
        reason: Optional[str] = None,
        purpose: Optional[str] = None,
        conditions: Optional[List[str]] = None,
        valid_from: Optional[str] = None,
        valid_until: Optional[str] = None,
    ) -> dict:
        """Create a permission assignment."""

        return self.engine.grant(
            permission_id=permission_id,
            granted_to=granted_to,
            resource=resource,
            action=action,
            scope=scope,
            granted_by=granted_by,
            reason=reason,
            purpose=purpose,
            conditions=conditions,
            valid_from=valid_from,
            valid_until=valid_until,
        )

    def list_permissions(self) -> dict:
        """Return all permission records."""

        return self.engine.list_permissions()

    def get_permission(
        self,
        permission_id: str,
    ) -> dict:
        """Return one permission record."""

        return self.engine.get_permission(
            permission_id
        )

    def approve(
        self,
        permission_id: str,
        approved_by: str,
    ) -> dict:
        """Approve a pending permission."""

        return self.engine.approve(
            permission_id=permission_id,
            approved_by=approved_by,
        )

    def activate(
        self,
        permission_id: str,
    ) -> dict:
        """Activate an approved permission."""

        return self.engine.activate(
            permission_id=permission_id,
        )

    def suspend(
        self,
        permission_id: str,
    ) -> dict:
        """Suspend an active permission."""

        return self.engine.suspend(
            permission_id=permission_id,
        )

    def revoke(
        self,
        permission_id: str,
        revoked_by: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> dict:
        """Revoke a permission."""

        return self.engine.revoke(
            permission_id=permission_id,
            revoked_by=revoked_by,
            reason=reason,
        )

    def connect(self) -> dict:
        """Connect the permission layer."""

        return self.engine.connect()

    def disconnect(self) -> dict:
        """Disconnect the permission layer."""

        return self.engine.disconnect()
