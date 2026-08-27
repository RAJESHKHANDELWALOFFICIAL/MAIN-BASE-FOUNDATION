"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Ownership Models

Central ownership and role-assignment models for ecosystem entities.

Hierarchy:

SUPREME
    ↓
Entity
    ↓
Primary Owner
    ↓
Owner
    ↓
Admin
    ↓
Manager / Moderator
    ↓
Member

Design principles:
- Entity creator becomes PRIMARY_OWNER.
- Ownership and administration are separate concepts.
- Roles are assigned explicitly.
- Permissions are explicit.
- Permission scope is explicit.
- Ownership transfer is controlled.
- SUPREME remains the master governance layer.
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

    return datetime.now(timezone.utc).isoformat()


# =========================================================
# 👑 ECOSYSTEM ROLE
# =========================================================

class EcosystemRole(str, Enum):
    """Supported ecosystem roles."""

    PRIMARY_OWNER = "PRIMARY_OWNER"
    OWNER = "OWNER"

    ADMIN = "ADMIN"

    MANAGER = "MANAGER"
    MODERATOR = "MODERATOR"

    EDITOR = "EDITOR"
    ANALYST = "ANALYST"

    MEMBER = "MEMBER"
    FOLLOWER = "FOLLOWER"


# =========================================================
# 🔐 OWNERSHIP STATUS
# =========================================================

class OwnershipStatus(str, Enum):
    """Ownership relationship status."""

    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    TRANSFER_PENDING = "TRANSFER_PENDING"
    TRANSFERRED = "TRANSFERRED"
    REVOKED = "REVOKED"
    REMOVED = "REMOVED"


# =========================================================
# 🎯 PERMISSION
# =========================================================

class EcosystemPermission(str, Enum):
    """Core ecosystem permissions."""

    VIEW = "VIEW"
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    MANAGE = "MANAGE"
    CONFIGURE = "CONFIGURE"

    MANAGE_PROFILE = "MANAGE_PROFILE"
    MANAGE_MEDIA = "MANAGE_MEDIA"

    MANAGE_CONTENT = "MANAGE_CONTENT"
    PUBLISH_CONTENT = "PUBLISH_CONTENT"
    DELETE_CONTENT = "DELETE_CONTENT"

    MANAGE_MEMBERS = "MANAGE_MEMBERS"

    ADD_OWNER = "ADD_OWNER"
    REMOVE_OWNER = "REMOVE_OWNER"

    ADD_ADMIN = "ADD_ADMIN"
    REMOVE_ADMIN = "REMOVE_ADMIN"

    CHANGE_ROLE = "CHANGE_ROLE"

    ASSIGN_PERMISSION = "ASSIGN_PERMISSION"
    REVOKE_PERMISSION = "REVOKE_PERMISSION"

    TRANSFER_OWNERSHIP = "TRANSFER_OWNERSHIP"
    ACCEPT_OWNERSHIP = "ACCEPT_OWNERSHIP"
    REJECT_OWNERSHIP = "REJECT_OWNERSHIP"

    MANAGE_SETTINGS = "MANAGE_SETTINGS"

    VIEW_ANALYTICS = "VIEW_ANALYTICS"

    MANAGE_INTEGRATIONS = "MANAGE_INTEGRATIONS"


# =========================================================
# 🌍 PERMISSION SCOPE
# =========================================================

class PermissionScope(str, Enum):
    """Scope at which a permission operates."""

    ENTITY = "ENTITY"
    PROFILE = "PROFILE"
    PAGE = "PAGE"
    GROUP = "GROUP"
    CHANNEL = "CHANNEL"
    COMMUNITY = "COMMUNITY"
    MEDIA = "MEDIA"
    CONTENT = "CONTENT"
    MEMBERS = "MEMBERS"
    SETTINGS = "SETTINGS"


# =========================================================
# 👤 OWNERSHIP ASSIGNMENT
# =========================================================

@dataclass
class OwnershipAssignment:
    """
    Represents a user's ownership or administrative
    relationship with an ecosystem entity.
    """

    assignment_id: str

    entity_id: str

    user_id: str

    role: EcosystemRole

    status: OwnershipStatus = OwnershipStatus.ACTIVE

    permissions: List[
        EcosystemPermission
    ] = field(default_factory=list)

    scopes: List[
        PermissionScope
    ] = field(default_factory=list)

    assigned_by: Optional[str] = None

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.assignment_id.strip():
            raise ValueError(
                "assignment_id cannot be empty."
            )

        if not self.entity_id.strip():
            raise ValueError(
                "entity_id cannot be empty."
            )

        if not self.user_id.strip():
            raise ValueError(
                "user_id cannot be empty."
            )

        if (
            self.role
            == EcosystemRole.PRIMARY_OWNER
            and self.status
            == OwnershipStatus.REVOKED
        ):
            raise ValueError(
                "PRIMARY_OWNER cannot be revoked "
                "through a normal ownership assignment."
            )


# =========================================================
# 🔐 ROLE PERMISSION
# =========================================================

@dataclass
class RolePermission:
    """
    Connect a role with an explicit permission and scope.
    """

    role: EcosystemRole

    permission: EcosystemPermission

    scope: PermissionScope = PermissionScope.ENTITY

    allowed: bool = True

    def __post_init__(self) -> None:

        if not isinstance(
            self.role,
            EcosystemRole,
        ):
            raise TypeError(
                "role must be an EcosystemRole."
            )

        if not isinstance(
            self.permission,
            EcosystemPermission,
        ):
            raise TypeError(
                "permission must be an "
                "EcosystemPermission."
            )

        if not isinstance(
            self.scope,
            PermissionScope,
        ):
            raise TypeError(
                "scope must be a PermissionScope."
            )


# =========================================================
# 🔄 OWNERSHIP TRANSFER
# =========================================================

@dataclass
class OwnershipTransfer:
    """
    Controlled ownership-transfer request.

    Ownership does not change merely because a transfer
    request is created. A transfer must be explicitly
    accepted/approved according to the authorization layer.
    """

    transfer_id: str

    entity_id: str

    current_owner_id: str

    new_owner_id: str

    status: OwnershipStatus = (
        OwnershipStatus.TRANSFER_PENDING
    )

    requested_by: Optional[str] = None

    approved_by: Optional[str] = None

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.transfer_id.strip():
            raise ValueError(
                "transfer_id cannot be empty."
            )

        if not self.entity_id.strip():
            raise ValueError(
                "entity_id cannot be empty."
            )

        if not self.current_owner_id.strip():
            raise ValueError(
                "current_owner_id cannot be empty."
            )

        if not self.new_owner_id.strip():
            raise ValueError(
                "new_owner_id cannot be empty."
            )

        if (
            self.current_owner_id
            == self.new_owner_id
        ):
            raise ValueError(
                "New owner must be different "
                "from current owner."
            )


# =========================================================
# 🛡️ ACCESS DECISION
# =========================================================

@dataclass(frozen=True)
class AccessDecision:
    """
    Result of an ecosystem authorization check.
    """

    allowed: bool

    user_id: str

    entity_id: str

    permission: EcosystemPermission

    scope: PermissionScope

    role: Optional[EcosystemRole] = None

    reason: str = ""


# =========================================================
# 👑 ENTITY OWNERSHIP
# =========================================================

@dataclass
class EntityOwnership:
    """
    Central ownership record for an ecosystem entity.

    The creator can be established as PRIMARY_OWNER.
    Additional owners and administrators can then be
    assigned through explicit authorization operations.
    """

    entity_id: str

    primary_owner_id: str

    assignments: List[
        OwnershipAssignment
    ] = field(default_factory=list)

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.entity_id.strip():
            raise ValueError(
                "entity_id cannot be empty."
            )

        if not self.primary_owner_id.strip():
            raise ValueError(
                "primary_owner_id cannot be empty."
            )

    def primary_owner(
        self,
    ) -> Optional[OwnershipAssignment]:
        """Return the PRIMARY_OWNER assignment."""

        for assignment in self.assignments:

            if (
                assignment.user_id
                == self.primary_owner_id
                and assignment.role
                == EcosystemRole.PRIMARY_OWNER
                and assignment.status
                == OwnershipStatus.ACTIVE
            ):
                return assignment

        return None

    def owners(
        self,
    ) -> List[OwnershipAssignment]:
        """Return active owner assignments."""

        return [
            assignment
            for assignment in self.assignments
            if assignment.role
            in (
                EcosystemRole.PRIMARY_OWNER,
                EcosystemRole.OWNER,
            )
            and assignment.status
            == OwnershipStatus.ACTIVE
        ]

    def admins(
        self,
    ) -> List[OwnershipAssignment]:
        """Return active administrator assignments."""

        return [
            assignment
            for assignment in self.assignments
            if assignment.role
            == EcosystemRole.ADMIN
            and assignment.status
            == OwnershipStatus.ACTIVE
        ]


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [

    # Roles
    "EcosystemRole",

    # Ownership
    "OwnershipStatus",
    "OwnershipAssignment",
    "EntityOwnership",
    "OwnershipTransfer",

    # Permissions
    "EcosystemPermission",
    "PermissionScope",
    "RolePermission",

    # Authorization
    "AccessDecision",
]
