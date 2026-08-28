"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Ownership Controller

Central control entry point for:
- Entity ownership
- Primary Owner
- Owners
- Admins
- Role management
- Permission management
- Ownership transfer
- Access verification

The controller delegates business rules to OwnershipService.
"""

from __future__ import annotations

from typing import List, Optional

from backend.supreme.ecosystem.ownership.model import (
    AccessDecision,
    EcosystemPermission,
    EcosystemRole,
    EntityOwnership,
    OwnershipAssignment,
    OwnershipTransfer,
    PermissionScope,
)

from backend.supreme.ecosystem.ownership.service import (
    OwnershipService,
)


class OwnershipController:
    """Central controller for ecosystem ownership."""

    def __init__(
        self,
        service: Optional[OwnershipService] = None,
    ) -> None:

        self.service = (
            service
            if service is not None
            else OwnershipService()
        )

    # =========================================================
    # 🚀 INITIALIZATION
    # =========================================================

    def initialize(self) -> dict:
        """Initialize ownership control."""

        return self.service.initialize()

    # =========================================================
    # 👑 CREATE OWNERSHIP
    # =========================================================

    def create_ownership(
        self,
        entity_id: str,
        primary_owner_id: str,
    ) -> EntityOwnership:
        """
        Create ownership for an entity.

        The creator becomes PRIMARY_OWNER.
        """

        return self.service.create_ownership(
            entity_id=entity_id,
            primary_owner_id=primary_owner_id,
        )

    # =========================================================
    # 🔎 GET OWNERSHIP
    # =========================================================

    def get_ownership(
        self,
        entity_id: str,
    ) -> Optional[EntityOwnership]:
        """Return entity ownership."""

        return self.service.get_ownership(
            entity_id
        )

    # =========================================================
    # 👑 ADD OWNER
    # =========================================================

    def add_owner(
        self,
        entity_id: str,
        user_id: str,
        assigned_by: str,
        permissions: Optional[
            List[EcosystemPermission]
        ] = None,
    ) -> OwnershipAssignment:
        """Add an OWNER."""

        return self.service.add_owner(
            entity_id=entity_id,
            user_id=user_id,
            assigned_by=assigned_by,
            permissions=permissions,
        )

    # =========================================================
    # 🛡️ ADD ADMIN
    # =========================================================

    def add_admin(
        self,
        entity_id: str,
        user_id: str,
        assigned_by: str,
        permissions: Optional[
            List[EcosystemPermission]
        ] = None,
    ) -> OwnershipAssignment:
        """Add an ADMIN."""

        return self.service.add_admin(
            entity_id=entity_id,
            user_id=user_id,
            assigned_by=assigned_by,
            permissions=permissions,
        )

    # =========================================================
    # 🔄 CHANGE ROLE
    # =========================================================

    def change_role(
        self,
        entity_id: str,
        user_id: str,
        new_role: EcosystemRole,
        changed_by: str,
    ) -> OwnershipAssignment:
        """Change a user's ecosystem role."""

        return self.service.change_role(
            entity_id=entity_id,
            user_id=user_id,
            new_role=new_role,
            changed_by=changed_by,
        )

    # =========================================================
    # ➕ ASSIGN PERMISSION
    # =========================================================

    def assign_permission(
        self,
        entity_id: str,
        user_id: str,
        permission: EcosystemPermission,
        assigned_by: str,
    ) -> OwnershipAssignment:
        """Assign a permission."""

        return self.service.assign_permission(
            entity_id=entity_id,
            user_id=user_id,
            permission=permission,
            assigned_by=assigned_by,
        )

    # =========================================================
    # ➖ REVOKE PERMISSION
    # =========================================================

    def revoke_permission(
        self,
        entity_id: str,
        user_id: str,
        permission: EcosystemPermission,
        revoked_by: str,
    ) -> OwnershipAssignment:
        """Revoke a permission."""

        return self.service.revoke_permission(
            entity_id=entity_id,
            user_id=user_id,
            permission=permission,
            revoked_by=revoked_by,
        )

    # =========================================================
    # ❌ REMOVE OWNER
    # =========================================================

    def remove_owner(
        self,
        entity_id: str,
        user_id: str,
        removed_by: str,
    ) -> bool:
        """Remove an OWNER."""

        return self.service.remove_owner(
            entity_id=entity_id,
            user_id=user_id,
            removed_by=removed_by,
        )

    # =========================================================
    # ❌ REMOVE ADMIN
    # =========================================================

    def remove_admin(
        self,
        entity_id: str,
        user_id: str,
        removed_by: str,
    ) -> bool:
        """Remove an ADMIN."""

        return self.service.remove_admin(
            entity_id=entity_id,
            user_id=user_id,
            removed_by=removed_by,
        )

    # =========================================================
    # 🔄 REQUEST OWNERSHIP TRANSFER
    # =========================================================

    def request_transfer(
        self,
        transfer: OwnershipTransfer,
    ) -> OwnershipTransfer:
        """
        Create an ownership-transfer request.
        """

        return self.service.request_transfer(
            transfer
        )

    # =========================================================
    # ✅ ACCEPT OWNERSHIP TRANSFER
    # =========================================================

    def accept_transfer(
        self,
        transfer_id: str,
        accepted_by: str,
    ) -> OwnershipTransfer:
        """
        Accept a pending ownership transfer.
        """

        return self.service.accept_transfer(
            transfer_id=transfer_id,
            accepted_by=accepted_by,
        )

    # =========================================================
    # 🔐 ACCESS CHECK
    # =========================================================

    def check_access(
        self,
        entity_id: str,
        user_id: str,
        permission: EcosystemPermission,
        scope: PermissionScope = (
            PermissionScope.ENTITY
        ),
    ) -> AccessDecision:
        """
        Check whether a user has a specific
        permission within a specific scope.
        """

        return self.service.check_access(
            entity_id=entity_id,
            user_id=user_id,
            permission=permission,
            scope=scope,
        )

    # =========================================================
    # 📋 LIST ASSIGNMENTS
    # =========================================================

    def list_assignments(
        self,
        entity_id: str,
    ) -> List[OwnershipAssignment]:
        """List active ownership/role assignments."""

        return self.service.list_assignments(
            entity_id
        )

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return ownership controller status."""

        return {
            "controller": (
                "SUPREME_ECOSYSTEM_OWNERSHIP"
            ),
            "service": self.service.status(),
        }


__all__ = [
    "OwnershipController",
]
