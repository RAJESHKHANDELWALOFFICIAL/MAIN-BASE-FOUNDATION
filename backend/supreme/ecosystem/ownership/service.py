"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Ownership Service

Central service for:
- Entity ownership
- Primary owner assignment
- Additional owners
- Administrators
- Role changes
- Permission assignment
- Permission revocation
- Ownership transfer requests
- Access checks

Design principle:

SUPREME remains the highest governance layer.

Individual ecosystem entities can have their own
Primary Owner, Owners, Admins and other delegated roles.
All delegated access is explicit and scoped.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from backend.supreme.ecosystem.ownership.model import (
    AccessDecision,
    EcosystemPermission,
    EcosystemRole,
    EntityOwnership,
    OwnershipAssignment,
    OwnershipStatus,
    OwnershipTransfer,
    PermissionScope,
)


class OwnershipService:
    """Central ownership and authorization service."""

    def __init__(self) -> None:

        self._ownership: Dict[
            str,
            EntityOwnership,
        ] = {}

        self._transfers: Dict[
            str,
            OwnershipTransfer,
        ] = {}

    # =========================================================
    # 🚀 INITIALIZATION
    # =========================================================

    def initialize(self) -> dict:
        """Initialize ownership service."""

        return {
            "service": "SUPREME_ECOSYSTEM_OWNERSHIP",
            "status": "READY",
        }

    # =========================================================
    # 👑 CREATE ENTITY OWNERSHIP
    # =========================================================

    def create_ownership(
        self,
        entity_id: str,
        primary_owner_id: str,
    ) -> EntityOwnership:
        """
        Create ownership for a new ecosystem entity.

        The creator is established as PRIMARY_OWNER.
        """

        self._validate_id(
            entity_id,
            "entity_id",
        )

        self._validate_id(
            primary_owner_id,
            "primary_owner_id",
        )

        if entity_id in self._ownership:
            raise ValueError(
                "Ownership already exists for this entity."
            )

        ownership = EntityOwnership(
            entity_id=entity_id,
            primary_owner_id=primary_owner_id,
        )

        primary_assignment = OwnershipAssignment(
            assignment_id=(
                f"{entity_id}:"
                f"{primary_owner_id}:"
                f"PRIMARY_OWNER"
            ),
            entity_id=entity_id,
            user_id=primary_owner_id,
            role=EcosystemRole.PRIMARY_OWNER,
            status=OwnershipStatus.ACTIVE,
            permissions=list(
                EcosystemPermission
            ),
            scopes=list(
                PermissionScope
            ),
            assigned_by="SUPREME",
        )

        ownership.assignments.append(
            primary_assignment
        )

        self._ownership[entity_id] = ownership

        return ownership

    # =========================================================
    # 🔎 GET OWNERSHIP
    # =========================================================

    def get_ownership(
        self,
        entity_id: str,
    ) -> Optional[EntityOwnership]:
        """Return ownership information."""

        return self._ownership.get(
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
        """Add an OWNER to an entity."""

        ownership = self._require_ownership(
            entity_id
        )

        self._require_permission(
            entity_id,
            assigned_by,
            EcosystemPermission.ADD_OWNER,
        )

        self._ensure_not_assigned(
            ownership,
            user_id,
        )

        assignment = OwnershipAssignment(
            assignment_id=(
                f"{entity_id}:"
                f"{user_id}:"
                f"OWNER"
            ),
            entity_id=entity_id,
            user_id=user_id,
            role=EcosystemRole.OWNER,
            permissions=(
                permissions
                if permissions is not None
                else self._default_owner_permissions()
            ),
            scopes=list(
                PermissionScope
            ),
            assigned_by=assigned_by,
        )

        ownership.assignments.append(
            assignment
        )

        return assignment

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
        """Add an ADMIN to an entity."""

        ownership = self._require_ownership(
            entity_id
        )

        self._require_permission(
            entity_id,
            assigned_by,
            EcosystemPermission.ADD_ADMIN,
        )

        self._ensure_not_assigned(
            ownership,
            user_id,
        )

        assignment = OwnershipAssignment(
            assignment_id=(
                f"{entity_id}:"
                f"{user_id}:"
                f"ADMIN"
            ),
            entity_id=entity_id,
            user_id=user_id,
            role=EcosystemRole.ADMIN,
            permissions=(
                permissions
                if permissions is not None
                else self._default_admin_permissions()
            ),
            scopes=[
                PermissionScope.ENTITY,
                PermissionScope.CONTENT,
                PermissionScope.MEMBERS,
                PermissionScope.MEDIA,
                PermissionScope.SETTINGS,
            ],
            assigned_by=assigned_by,
        )

        ownership.assignments.append(
            assignment
        )

        return assignment

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
        """
        Change an assigned user's role.

        PRIMARY_OWNER is protected from ordinary role changes.
        """

        ownership = self._require_ownership(
            entity_id
        )

        self._require_permission(
            entity_id,
            changed_by,
            EcosystemPermission.CHANGE_ROLE,
        )

        assignment = self._find_assignment(
            ownership,
            user_id,
        )

        if assignment is None:
            raise ValueError(
                "User has no active assignment "
                "for this entity."
            )

        if (
            assignment.role
            == EcosystemRole.PRIMARY_OWNER
        ):
            raise ValueError(
                "PRIMARY_OWNER cannot be changed "
                "through normal role management."
            )

        assignment.role = new_role
        assignment.updated_at = (
            self._now()
        )

        return assignment

    # =========================================================
    # ➕ ADD PERMISSION
    # =========================================================

    def assign_permission(
        self,
        entity_id: str,
        user_id: str,
        permission: EcosystemPermission,
        assigned_by: str,
    ) -> OwnershipAssignment:
        """Assign a permission to a user."""

        ownership = self._require_ownership(
            entity_id
        )

        self._require_permission(
            entity_id,
            assigned_by,
            EcosystemPermission.ASSIGN_PERMISSION,
        )

        assignment = self._find_assignment(
            ownership,
            user_id,
        )

        if assignment is None:
            raise ValueError(
                "User has no active assignment."
            )

        if permission not in assignment.permissions:
            assignment.permissions.append(
                permission
            )

        assignment.updated_at = (
            self._now()
        )

        return assignment

    # =========================================================
    # ➖ REMOVE PERMISSION
    # =========================================================

    def revoke_permission(
        self,
        entity_id: str,
        user_id: str,
        permission: EcosystemPermission,
        revoked_by: str,
    ) -> OwnershipAssignment:
        """Revoke a permission from a user."""

        ownership = self._require_ownership(
            entity_id
        )

        self._require_permission(
            entity_id,
            revoked_by,
            EcosystemPermission.REVOKE_PERMISSION,
        )

        assignment = self._find_assignment(
            ownership,
            user_id,
        )

        if assignment is None:
            raise ValueError(
                "User has no active assignment."
            )

        if (
            assignment.role
            == EcosystemRole.PRIMARY_OWNER
        ):
            raise ValueError(
                "PRIMARY_OWNER permissions cannot "
                "be revoked through normal delegation."
            )

        if permission in assignment.permissions:
            assignment.permissions.remove(
                permission
            )

        assignment.updated_at = (
            self._now()
        )

        return assignment

    # =========================================================
    # ❌ REMOVE OWNER
    # =========================================================

    def remove_owner(
        self,
        entity_id: str,
        user_id: str,
        removed_by: str,
    ) -> bool:
        """Remove an OWNER assignment."""

        ownership = self._require_ownership(
            entity_id
        )

        self._require_permission(
            entity_id,
            removed_by,
            EcosystemPermission.REMOVE_OWNER,
        )

        assignment = self._find_assignment(
            ownership,
            user_id,
        )

        if assignment is None:
            return False

        if (
            assignment.role
            == EcosystemRole.PRIMARY_OWNER
        ):
            raise ValueError(
                "PRIMARY_OWNER cannot be removed "
                "through normal owner removal."
            )

        if (
            assignment.role
            != EcosystemRole.OWNER
        ):
            raise ValueError(
                "User is not an OWNER."
            )

        assignment.status = (
            OwnershipStatus.REMOVED
        )

        assignment.updated_at = (
            self._now()
        )

        return True

    # =========================================================
    # ❌ REMOVE ADMIN
    # =========================================================

    def remove_admin(
        self,
        entity_id: str,
        user_id: str,
        removed_by: str,
    ) -> bool:
        """Remove an ADMIN assignment."""

        ownership = self._require_ownership(
            entity_id
        )

        self._require_permission(
            entity_id,
            removed_by,
            EcosystemPermission.REMOVE_ADMIN,
        )

        assignment = self._find_assignment(
            ownership,
            user_id,
        )

        if assignment is None:
            return False

        if (
            assignment.role
            != EcosystemRole.ADMIN
        ):
            raise ValueError(
                "User is not an ADMIN."
            )

        assignment.status = (
            OwnershipStatus.REMOVED
        )

        assignment.updated_at = (
            self._now()
        )

        return True

    # =========================================================
    # 🔄 OWNERSHIP TRANSFER REQUEST
    # =========================================================

    def request_transfer(
        self,
        transfer: OwnershipTransfer,
    ) -> OwnershipTransfer:
        """
        Create an ownership transfer request.

        Creating a request does NOT immediately transfer
        ownership.
        """

        ownership = self._require_ownership(
            transfer.entity_id
        )

        self._require_permission(
            transfer.entity_id,
            transfer.requested_by
            or transfer.current_owner_id,
            EcosystemPermission.TRANSFER_OWNERSHIP,
        )

        if (
            ownership.primary_owner_id
            != transfer.current_owner_id
        ):
            raise ValueError(
                "Current owner does not match "
                "the entity PRIMARY_OWNER."
            )

        self._transfers[
            transfer.transfer_id
        ] = transfer

        return transfer

    # =========================================================
    # ✅ ACCEPT TRANSFER
    # =========================================================

    def accept_transfer(
        self,
        transfer_id: str,
        accepted_by: str,
    ) -> OwnershipTransfer:
        """
        Accept an ownership transfer.

        The transfer must be explicitly approved.
        """

        transfer = self._transfers.get(
            transfer_id
        )

        if transfer is None:
            raise ValueError(
                "Ownership transfer not found."
            )

        if (
            transfer.new_owner_id
            != accepted_by
        ):
            raise PermissionError(
                "Only the proposed new owner "
                "can accept this transfer."
            )

        if (
            transfer.status
            != OwnershipStatus.TRANSFER_PENDING
        ):
            raise ValueError(
                "Transfer is not pending."
            )

        ownership = self._require_ownership(
            transfer.entity_id
        )

        old_assignment = self._find_assignment(
            ownership,
            transfer.current_owner_id,
        )

        if old_assignment is not None:
            old_assignment.role = (
                EcosystemRole.OWNER
            )
            old_assignment.updated_at = (
                self._now()
            )

        new_assignment = self._find_assignment(
            ownership,
            transfer.new_owner_id,
        )

        if new_assignment is None:

            new_assignment = OwnershipAssignment(
                assignment_id=(
                    f"{transfer.entity_id}:"
                    f"{transfer.new_owner_id}:"
                    f"PRIMARY_OWNER"
                ),
                entity_id=transfer.entity_id,
                user_id=transfer.new_owner_id,
                role=EcosystemRole.PRIMARY_OWNER,
                status=OwnershipStatus.ACTIVE,
                permissions=list(
                    EcosystemPermission
                ),
                scopes=list(
                    PermissionScope
                ),
                assigned_by="SUPREME",
            )

            ownership.assignments.append(
                new_assignment
            )

        else:
            new_assignment.role = (
                EcosystemRole.PRIMARY_OWNER
            )
            new_assignment.status = (
                OwnershipStatus.ACTIVE
            )

        ownership.primary_owner_id = (
            transfer.new_owner_id
        )

        ownership.updated_at = (
            self._now()
        )

        transfer.status = (
            OwnershipStatus.TRANSFERRED
        )

        transfer.approved_by = accepted_by
        transfer.updated_at = (
            self._now()
        )

        return transfer

    # =========================================================
    # 🔎 ACCESS CHECK
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
        """Check whether a user has a permission."""

        ownership = self._ownership.get(
            entity_id
        )

        if ownership is None:
            return AccessDecision(
                allowed=False,
                user_id=user_id,
                entity_id=entity_id,
                permission=permission,
                scope=scope,
                reason="Entity ownership not found.",
            )

        assignment = self._find_assignment(
            ownership,
            user_id,
        )

        if assignment is None:
            return AccessDecision(
                allowed=False,
                user_id=user_id,
                entity_id=entity_id,
                permission=permission,
                scope=scope,
                reason="No active role assignment.",
            )

        if (
            permission
            not in assignment.permissions
        ):
            return AccessDecision(
                allowed=False,
                user_id=user_id,
                entity_id=entity_id,
                permission=permission,
                scope=scope,
                role=assignment.role,
                reason="Permission not assigned.",
            )

        if (
            scope
            not in assignment.scopes
        ):
            return AccessDecision(
                allowed=False,
                user_id=user_id,
                entity_id=entity_id,
                permission=permission,
                scope=scope,
                role=assignment.role,
                reason="Permission scope not assigned.",
            )

        return AccessDecision(
            allowed=True,
            user_id=user_id,
            entity_id=entity_id,
            permission=permission,
            scope=scope,
            role=assignment.role,
            reason="Access granted.",
        )

    # =========================================================
    # 📋 LIST ASSIGNMENTS
    # =========================================================

    def list_assignments(
        self,
        entity_id: str,
    ) -> List[OwnershipAssignment]:
        """Return active assignments."""

        ownership = self._require_ownership(
            entity_id
        )

        return [
            assignment
            for assignment in ownership.assignments
            if assignment.status
            == OwnershipStatus.ACTIVE
        ]

    # =========================================================
    # 🧩 DEFAULT PERMISSIONS
    # =========================================================

    def _default_owner_permissions(
        self,
    ) -> List[EcosystemPermission]:

        return [
            EcosystemPermission.VIEW,
            EcosystemPermission.READ,
            EcosystemPermission.UPDATE,
            EcosystemPermission.MANAGE,
            EcosystemPermission.MANAGE_PROFILE,
            EcosystemPermission.MANAGE_MEDIA,
            EcosystemPermission.MANAGE_CONTENT,
            EcosystemPermission.PUBLISH_CONTENT,
            EcosystemPermission.MANAGE_MEMBERS,
            EcosystemPermission.ADD_OWNER,
            EcosystemPermission.REMOVE_OWNER,
            EcosystemPermission.ADD_ADMIN,
            EcosystemPermission.REMOVE_ADMIN,
            EcosystemPermission.CHANGE_ROLE,
            EcosystemPermission.ASSIGN_PERMISSION,
            EcosystemPermission.REVOKE_PERMISSION,
            EcosystemPermission.TRANSFER_OWNERSHIP,
            EcosystemPermission.VIEW_ANALYTICS,
            EcosystemPermission.MANAGE_SETTINGS,
            EcosystemPermission.MANAGE_INTEGRATIONS,
        ]

    def _default_admin_permissions(
        self,
    ) -> List[EcosystemPermission]:

        return [
            EcosystemPermission.VIEW,
            EcosystemPermission.READ,
            EcosystemPermission.UPDATE,
            EcosystemPermission.MANAGE_PROFILE,
            EcosystemPermission.MANAGE_MEDIA,
            EcosystemPermission.MANAGE_CONTENT,
            EcosystemPermission.PUBLISH_CONTENT,
            EcosystemPermission.MANAGE_MEMBERS,
            EcosystemPermission.VIEW_ANALYTICS,
            EcosystemPermission.MANAGE_SETTINGS,
        ]

    # =========================================================
    # 🔎 INTERNAL HELPERS
    # =========================================================

    def _require_ownership(
        self,
        entity_id: str,
    ) -> EntityOwnership:

        ownership = self._ownership.get(
            entity_id
        )

        if ownership is None:
            raise ValueError(
                "Entity ownership not found."
            )

        return ownership

    def _find_assignment(
        self,
        ownership: EntityOwnership,
        user_id: str,
    ) -> Optional[OwnershipAssignment]:

        for assignment in ownership.assignments:

            if (
                assignment.user_id
                == user_id
                and assignment.status
                == OwnershipStatus.ACTIVE
            ):
                return assignment

        return None

    def _ensure_not_assigned(
        self,
        ownership: EntityOwnership,
        user_id: str,
    ) -> None:

        assignment = self._find_assignment(
            ownership,
            user_id,
        )

        if assignment is not None:
            raise ValueError(
                "User already has an active "
                "assignment for this entity."
            )

    def _require_permission(
        self,
        entity_id: str,
        user_id: str,
        permission: EcosystemPermission,
    ) -> None:
        """
        Verify that a user can perform an operation.

        SUPREME itself is treated as the master governance
        authority for internal system operations.
        """

        if user_id == "SUPREME":
            return

        decision = self.check_access(
            entity_id=entity_id,
            user_id=user_id,
            permission=permission,
            scope=PermissionScope.ENTITY,
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

    @staticmethod
    def _validate_id(
        value: str,
        field_name: str,
    ) -> None:

        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def _now() -> str:

        from datetime import datetime, timezone

        return datetime.now(
            timezone.utc
        ).isoformat()

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return ownership service status."""

        return {
            "service": "OwnershipService",
            "entities": len(
                self._ownership
            ),
            "transfers": len(
                self._transfers
            ),
            "status": "READY",
        }


__all__ = [
    "OwnershipService",
]
