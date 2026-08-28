"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Ownership Models

Central ownership, role and permission models for:

- Personal Profiles
- Professional Profiles
- Pages
- Groups
- Channels
- Communities
- Future Ecosystem Entities

Ownership hierarchy:

SUPREME
    ↓
PRIMARY_OWNER
    ↓
OWNER
    ↓
ADMIN
    ↓
MANAGER
    ↓
MODERATOR
    ↓
MEMBER

Design principles:

- Every ecosystem entity has explicit ownership.
- The creator becomes PRIMARY_OWNER.
- PRIMARY_OWNER has the highest entity-level authority.
- OWNER and ADMIN access is permission based.
- Permissions can be assigned, changed and revoked.
- Ownership can be transferred through an explicit operation.
- SUPREME governance remains above individual ecosystem entities.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional


# =========================================================
# 🕐 TIME
# =========================================================

def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(
        timezone.utc
    ).isoformat()


# =========================================================
# 👑 ECOSYSTEM ROLE
# =========================================================

class EcosystemRole(str, Enum):
    """Roles available inside an ecosystem entity."""

    PRIMARY_OWNER = "PRIMARY_OWNER"
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    MODERATOR = "MODERATOR"
    MEMBER = "MEMBER"


# =========================================================
# 📊 OWNERSHIP STATUS
# =========================================================

class OwnershipStatus(str, Enum):
    """Ownership assignment status."""

    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    TRANSFER_PENDING = "TRANSFER_PENDING"
    TRANSFERRED = "TRANSFERRED"
    REMOVED = "REMOVED"


# =========================================================
# 🔐 PERMISSION
# =========================================================

class EcosystemPermission(str, Enum):
    """Permissions available inside an ecosystem entity."""

    VIEW = "VIEW"
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    MANAGE = "MANAGE"
    CONFIGURE = "CONFIGURE"

    MANAGE_PROFILE = "MANAGE_PROFILE"
    MANAGE_PAGE = "MANAGE_PAGE"
    MANAGE_GROUP = "MANAGE_GROUP"
    MANAGE_CHANNEL = "MANAGE_CHANNEL"
    MANAGE_COMMUNITY = "MANAGE_COMMUNITY"

    MANAGE_MEDIA = "MANAGE_MEDIA"

    MANAGE_MEMBERS = "MANAGE_MEMBERS"
    MANAGE_ROLES = "MANAGE_ROLES"
    MANAGE_PERMISSIONS = "MANAGE_PERMISSIONS"

    ADD_OWNER = "ADD_OWNER"
    REMOVE_OWNER = "REMOVE_OWNER"

    ADD_ADMIN = "ADD_ADMIN"
    REMOVE_ADMIN = "REMOVE_ADMIN"

    CHANGE_ROLE = "CHANGE_ROLE"
    TRANSFER_OWNERSHIP = "TRANSFER_OWNERSHIP"


# =========================================================
# 🎯 PERMISSION SCOPE
# =========================================================

class PermissionScope(str, Enum):
    """Scope in which a permission applies."""

    ENTITY = "ENTITY"
    PROFILE = "PROFILE"
    PAGE = "PAGE"
    GROUP = "GROUP"
    CHANNEL = "CHANNEL"
    COMMUNITY = "COMMUNITY"
    MEDIA = "MEDIA"
    MEMBERS = "MEMBERS"
    ROLES = "ROLES"
    PERMISSIONS = "PERMISSIONS"


# =========================================================
# 🔗 ROLE PERMISSION
# =========================================================

@dataclass
class RolePermission:
    """Permission assigned to a role."""

    role: EcosystemRole

    permission: EcosystemPermission

    scope: PermissionScope = (
        PermissionScope.ENTITY
    )

    enabled: bool = True

    created_at: str = field(
        default_factory=utc_now
    )

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
# 👤 OWNERSHIP ASSIGNMENT
# =========================================================

@dataclass
class OwnershipAssignment:
    """
    Assignment of a role to a user inside an entity.
    """

    entity_id: str

    user_id: str

    role: EcosystemRole

    permissions: List[
        EcosystemPermission
    ] = field(default_factory=list)

    status: OwnershipStatus = (
        OwnershipStatus.ACTIVE
    )

    assigned_by: Optional[str] = None

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

        if not self.user_id.strip():
            raise ValueError(
                "user_id cannot be empty."
            )

        if not isinstance(
            self.role,
            EcosystemRole,
        ):
            raise TypeError(
                "role must be an EcosystemRole."
            )

        if self.assigned_by is not None:

            if not self.assigned_by.strip():
                raise ValueError(
                    "assigned_by cannot be empty."
                )


# =========================================================
# 👑 ENTITY OWNERSHIP
# =========================================================

@dataclass
class EntityOwnership:
    """
    Complete ownership record for one ecosystem entity.

    One entity has exactly one PRIMARY_OWNER at a time.
    Additional OWNER and ADMIN assignments are maintained
    separately.
    """

    entity_id: str

    primary_owner_id: str

    assignments: List[
        OwnershipAssignment
    ] = field(default_factory=list)

    status: OwnershipStatus = (
        OwnershipStatus.ACTIVE
    )

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

    def has_user(
        self,
        user_id: str,
    ) -> bool:
        """Return whether the user has an assignment."""

        return any(
            assignment.user_id == user_id
            and assignment.status
            == OwnershipStatus.ACTIVE
            for assignment in self.assignments
        )

    def get_assignment(
        self,
        user_id: str,
    ) -> Optional[OwnershipAssignment]:
        """Return a user's active assignment."""

        for assignment in self.assignments:

            if (
                assignment.user_id == user_id
                and assignment.status
                == OwnershipStatus.ACTIVE
            ):
                return assignment

        return None


# =========================================================
# 🔄 OWNERSHIP TRANSFER
# =========================================================

@dataclass
class OwnershipTransfer:
    """
    Explicit ownership transfer request.
    """

    transfer_id: str

    entity_id: str

    current_owner_id: str

    new_owner_id: str

    status: OwnershipStatus = (
        OwnershipStatus.TRANSFER_PENDING
    )

    requested_at: str = field(
        default_factory=utc_now
    )

    completed_at: Optional[str] = None

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
                "new_owner_id must be different "
                "from current_owner_id."
            )


# =========================================================
# 🔎 ACCESS DECISION
# =========================================================

@dataclass(frozen=True)
class AccessDecision:
    """
    Result of an ecosystem permission check.
    """

    entity_id: str

    user_id: str

    permission: EcosystemPermission

    allowed: bool

    role: Optional[
        EcosystemRole
    ] = None

    scope: PermissionScope = (
        PermissionScope.ENTITY
    )

    reason: str = ""


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

    # Access
    "AccessDecision",
]
