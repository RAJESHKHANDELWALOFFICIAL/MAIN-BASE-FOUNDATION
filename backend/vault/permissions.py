"""
MAIN BASE FOUNDATION
Secure Vault — Authorization Policy

SUPREME OWNER is the master authorized controller of
the MAIN BASE FOUNDATION.

The Secure Vault remains its own module, while authorization
can be granted through the central SUPREME ownership layer.

Security principles:

- DENY BY DEFAULT
- AUTHENTICATION REQUIRED
- AUTHORIZATION REQUIRED
- SUPREME OWNER = HIGHEST AUTHORIZED OWNER
- SUPREME PROFILE = OWNER ONLY
- NO FRONTEND-ONLY SECURITY
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Optional


# =========================================================
# 🔐 VAULT ACTIONS
# =========================================================

class VaultAction(str, Enum):
    """Actions available inside the Secure Vault."""

    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    SEARCH = "search"
    EXPORT = "export"

    MANAGE_ACCESS = "manage_access"
    MANAGE_SECURITY = "manage_security"


# =========================================================
# 👤 PRINCIPAL TYPES
# =========================================================

class PrincipalType(str, Enum):
    """
    Identity types that may request access.
    """

    SUPREME_OWNER = "supreme_owner"
    USER = "user"
    SERVICE = "service"
    SYSTEM = "system"


# =========================================================
# 👑 PROFILE VISIBILITY
# =========================================================

class ProfileVisibility(str, Enum):
    """Visibility policies for protected profiles."""

    OWNER_ONLY = "owner_only"
    PRIVATE = "private"
    INTERNAL = "internal"


# =========================================================
# 🔑 PERMISSION SET
# =========================================================

@dataclass(frozen=True)
class PermissionSet:
    """
    Immutable set of explicitly authorized actions.
    """

    actions: FrozenSet[VaultAction]

    def allows(
        self,
        action: VaultAction,
    ) -> bool:
        """Return True when the action is authorized."""

        return action in self.actions


# =========================================================
# 👑 SUPREME OWNER — VAULT PERMISSIONS
# =========================================================

SUPREME_OWNER_VAULT_PERMISSIONS = PermissionSet(
    actions=frozenset(
        {
            VaultAction.READ,
            VaultAction.CREATE,
            VaultAction.UPDATE,
            VaultAction.DELETE,
            VaultAction.SEARCH,
            VaultAction.EXPORT,
            VaultAction.MANAGE_ACCESS,
            VaultAction.MANAGE_SECURITY,
        }
    )
)


# =========================================================
# 👤 DEFAULT USER — DENY BY DEFAULT
# =========================================================

DEFAULT_USER_VAULT_PERMISSIONS = PermissionSet(
    actions=frozenset()
)


# =========================================================
# 🔐 ACCESS REQUEST
# =========================================================

@dataclass(frozen=True)
class VaultAccessRequest:
    """
    Server-side request for Vault authorization.
    """

    principal_id: str
    principal_type: PrincipalType

    vault_id: str
    action: VaultAction

    resource_id: Optional[str] = None

    authenticated: bool = False

    supreme_owner_verified: bool = False

    def __post_init__(self) -> None:

        if not self.principal_id.strip():
            raise ValueError(
                "Principal ID cannot be empty."
            )

        if not self.vault_id.strip():
            raise ValueError(
                "Vault ID cannot be empty."
            )


# =========================================================
# 🛡️ AUTHORIZATION RESULT
# =========================================================

@dataclass(frozen=True)
class AuthorizationResult:
    """
    Result returned by the authorization layer.
    """

    allowed: bool

    reason: str

    principal_id: str

    action: VaultAction

    resource_id: Optional[str] = None


# =========================================================
# 👑 SUPREME PROFILE POLICY
# =========================================================

@dataclass(frozen=True)
class SupremeProfilePolicy:
    """
    Owner-only policy for the SUPREME profile.

    The profile must never be treated as public data.
    """

    owner_id: str

    visibility: ProfileVisibility = (
        ProfileVisibility.OWNER_ONLY
    )

    def __post_init__(self) -> None:

        if not self.owner_id.strip():
            raise ValueError(
                "Supreme owner ID cannot be empty."
            )

        if (
            self.visibility
            != ProfileVisibility.OWNER_ONLY
        ):
            raise ValueError(
                "Supreme profile must remain owner-only."
            )


# =========================================================
# 👑 CENTRAL SUPREME AUTHORIZATION BRIDGE
# =========================================================

class SupremeAuthorizationBridge:
    """
    Authorization bridge between SUPREME ownership and
    protected MAIN BASE FOUNDATION services.

    The bridge does not authenticate a user itself.

    Authentication must be completed by the Identity /
    Authentication system first.
    """

    def __init__(
        self,
        supreme_owner_id: str,
    ) -> None:

        if not supreme_owner_id.strip():
            raise ValueError(
                "Supreme owner ID cannot be empty."
            )

        self._supreme_owner_id = (
            supreme_owner_id
        )

    # =====================================================
    # 👑 VERIFY SUPREME OWNER
    # =====================================================

    def is_verified_supreme_owner(
        self,
        principal_id: str,
        authenticated: bool,
        supreme_owner_verified: bool,
    ) -> bool:
        """
        Confirm that the authenticated principal is the
        configured Supreme Owner.
        """

        if not authenticated:
            return False

        if not supreme_owner_verified:
            return False

        return (
            principal_id
            == self._supreme_owner_id
        )

    # =====================================================
    # 🔑 RESOLVE VAULT PERMISSIONS
    # =====================================================

    def resolve_vault_permissions(
        self,
        principal_id: str,
        principal_type: PrincipalType,
        authenticated: bool,
        supreme_owner_verified: bool,
    ) -> PermissionSet:
        """
        Resolve Vault permissions.

        Supreme Owner receives all currently defined Vault
        permissions after successful authentication and
        owner verification.

        All other identities receive no permission by
        default.
        """

        if not authenticated:
            return DEFAULT_USER_VAULT_PERMISSIONS

        if (
            principal_type
            == PrincipalType.SUPREME_OWNER
            and self.is_verified_supreme_owner(
                principal_id=principal_id,
                authenticated=authenticated,
                supreme_owner_verified=(
                    supreme_owner_verified
                ),
            )
        ):
            return SUPREME_OWNER_VAULT_PERMISSIONS

        return DEFAULT_USER_VAULT_PERMISSIONS

    # =====================================================
    # 🔐 AUTHORIZE VAULT ACTION
    # =====================================================

    def authorize_vault(
        self,
        request: VaultAccessRequest,
    ) -> AuthorizationResult:
        """
        Authorize a specific Vault operation.
        """

        permissions = (
            self.resolve_vault_permissions(
                principal_id=request.principal_id,
                principal_type=request.principal_type,
                authenticated=request.authenticated,
                supreme_owner_verified=(
                    request.supreme_owner_verified
                ),
            )
        )

        if permissions.allows(
            request.action
        ):
            return AuthorizationResult(
                allowed=True,
                reason=(
                    "Vault permission granted."
                ),
                principal_id=(
                    request.principal_id
                ),
                action=request.action,
                resource_id=request.resource_id,
            )

        return AuthorizationResult(
            allowed=False,
            reason="Vault access denied.",
            principal_id=(
                request.principal_id
            ),
            action=request.action,
            resource_id=request.resource_id,
        )

    # =====================================================
    # 👑 AUTHORIZE SUPREME PROFILE
    # =====================================================

    def authorize_supreme_profile(
        self,
        principal_id: str,
        authenticated: bool,
        supreme_owner_verified: bool,
    ) -> AuthorizationResult:
        """
        Authorize access to the private SUPREME profile.

        Only the verified configured Supreme Owner can
        receive authorization.
        """

        if not authenticated:
            return AuthorizationResult(
                allowed=False,
                reason="Authentication required.",
                principal_id=principal_id,
                action=VaultAction.READ,
            )

        if not supreme_owner_verified:
            return AuthorizationResult(
                allowed=False,
                reason=(
                    "Supreme Owner verification required."
                ),
                principal_id=principal_id,
                action=VaultAction.READ,
            )

        if principal_id != self._supreme_owner_id:
            return AuthorizationResult(
                allowed=False,
                reason=(
                    "Supreme profile is owner-only."
                ),
                principal_id=principal_id,
                action=VaultAction.READ,
            )

        return AuthorizationResult(
            allowed=True,
            reason=(
                "Supreme Owner profile access granted."
            ),
            principal_id=principal_id,
            action=VaultAction.READ,
        )


# =========================================================
# 🚫 SAFE DEFAULT
# =========================================================

def deny_by_default(
    principal_id: str,
    action: VaultAction,
) -> AuthorizationResult:
    """
    Explicit safe-denial helper.
    """

    return AuthorizationResult(
        allowed=False,
        reason="Access denied by default.",
        principal_id=principal_id,
        action=action,
    )


# =========================================================
# 📊 AUTHORIZATION STATUS
# =========================================================

def authorization_status() -> dict:
    """
    Return authorization subsystem metadata.
    """

    return {
        "service": "secure_vault_authorization",
        "model": "deny_by_default",
        "supreme_owner": "master_authorized_controller",
        "supreme_profile": "owner_only",
        "frontend_only_security": False,
        "authentication_required": True,
        "authorization_required": True,
    }


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "VaultAction",
    "PrincipalType",
    "ProfileVisibility",
    "PermissionSet",
    "VaultAccessRequest",
    "AuthorizationResult",
    "SupremeProfilePolicy",
    "SupremeAuthorizationBridge",
    "SUPREME_OWNER_VAULT_PERMISSIONS",
    "DEFAULT_USER_VAULT_PERMISSIONS",
    "deny_by_default",
    "authorization_status",
]
