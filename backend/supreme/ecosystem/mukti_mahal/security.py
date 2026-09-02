"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Security

Security and access-control layer for the Mukti Mahal ecosystem.

Handles:
- roles
- permissions
- access decisions
- security policies
- audit events

No passwords, OTPs, API keys, tokens, payment credentials,
or other authentication secrets are stored here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Set


def _utc_now() -> datetime:
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc)


class SecurityRole(str, Enum):
    """Security roles used by the ecosystem."""

    SYSTEM_ADMIN = "SYSTEM_ADMIN"
    MAHAL_ADMIN = "MAHAL_ADMIN"
    ESTATE_MANAGER = "ESTATE_MANAGER"
    BUSINESS_MANAGER = "BUSINESS_MANAGER"
    EXECUTIVE = "EXECUTIVE"
    BOARD_MEMBER = "BOARD_MEMBER"
    FAMILY_MEMBER = "FAMILY_MEMBER"
    STAFF = "STAFF"
    REVIEWER = "REVIEWER"
    CREATOR = "CREATOR"
    USER = "USER"


class SecurityPermission(str, Enum):
    """Fine-grained platform permissions."""

    VIEW_MAHAL = "VIEW_MAHAL"
    MANAGE_MAHAL = "MANAGE_MAHAL"

    VIEW_FAMILY = "VIEW_FAMILY"
    MANAGE_FAMILY = "MANAGE_FAMILY"

    VIEW_STAFF = "VIEW_STAFF"
    MANAGE_STAFF = "MANAGE_STAFF"

    VIEW_ESTATE = "VIEW_ESTATE"
    MANAGE_ESTATE = "MANAGE_ESTATE"

    VIEW_BUSINESS = "VIEW_BUSINESS"
    MANAGE_BUSINESS = "MANAGE_BUSINESS"

    VIEW_BOARD = "VIEW_BOARD"
    MANAGE_BOARD = "MANAGE_BOARD"

    VIEW_VERIFICATION = "VIEW_VERIFICATION"
    MANAGE_VERIFICATION = "MANAGE_VERIFICATION"

    VIEW_MODERATION = "VIEW_MODERATION"
    MANAGE_MODERATION = "MANAGE_MODERATION"

    VIEW_MONETIZATION = "VIEW_MONETIZATION"
    MANAGE_MONETIZATION = "MANAGE_MONETIZATION"

    VIEW_AUDIT = "VIEW_AUDIT"


class SecurityDecision(str, Enum):
    """Result of an access-control decision."""

    ALLOW = "ALLOW"
    DENY = "DENY"


@dataclass
class SecurityPrincipal:
    """Represents an actor requesting access."""

    principal_id: str
    roles: Set[SecurityRole] = field(default_factory=set)
    active: bool = True

    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.principal_id:
            raise ValueError("principal_id is required")


@dataclass
class SecurityAuditEvent:
    """Represents a security-related audit event."""

    event_id: str
    principal_id: str
    action: str
    resource_type: str
    resource_id: Optional[str] = None

    decision: SecurityDecision = SecurityDecision.ALLOW
    reason: str = ""

    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.event_id:
            raise ValueError("event_id is required")

        if not self.principal_id:
            raise ValueError("principal_id is required")

        if not self.action:
            raise ValueError("action is required")

        if not self.resource_type:
            raise ValueError("resource_type is required")


@dataclass
class SecurityPolicy:
    """Global security policy."""

    deny_inactive_principals: bool = True
    audit_access_decisions: bool = True
    least_privilege_required: bool = True


class MuktiMahalSecurity:
    """Central security and access-control service."""

    ROLE_PERMISSIONS: Dict[
        SecurityRole,
        Set[SecurityPermission],
    ] = {
        SecurityRole.SYSTEM_ADMIN: set(SecurityPermission),

        SecurityRole.MAHAL_ADMIN: {
            SecurityPermission.VIEW_MAHAL,
            SecurityPermission.MANAGE_MAHAL,
            SecurityPermission.VIEW_FAMILY,
            SecurityPermission.MANAGE_FAMILY,
            SecurityPermission.VIEW_STAFF,
            SecurityPermission.MANAGE_STAFF,
            SecurityPermission.VIEW_ESTATE,
            SecurityPermission.MANAGE_ESTATE,
            SecurityPermission.VIEW_BUSINESS,
            SecurityPermission.MANAGE_BUSINESS,
            SecurityPermission.VIEW_BOARD,
            SecurityPermission.MANAGE_BOARD,
            SecurityPermission.VIEW_VERIFICATION,
            SecurityPermission.VIEW_MODERATION,
            SecurityPermission.VIEW_AUDIT,
        },

        SecurityRole.ESTATE_MANAGER: {
            SecurityPermission.VIEW_MAHAL,
            SecurityPermission.VIEW_FAMILY,
            SecurityPermission.VIEW_STAFF,
            SecurityPermission.MANAGE_STAFF,
            SecurityPermission.VIEW_ESTATE,
            SecurityPermission.MANAGE_ESTATE,
        },

        SecurityRole.BUSINESS_MANAGER: {
            SecurityPermission.VIEW_MAHAL,
            SecurityPermission.VIEW_BUSINESS,
            SecurityPermission.MANAGE_BUSINESS,
            SecurityPermission.VIEW_BOARD,
        },

        SecurityRole.EXECUTIVE: {
            SecurityPermission.VIEW_MAHAL,
            SecurityPermission.VIEW_BUSINESS,
            SecurityPermission.MANAGE_BUSINESS,
            SecurityPermission.VIEW_BOARD,
        },

        SecurityRole.BOARD_MEMBER: {
            SecurityPermission.VIEW_MAHAL,
            SecurityPermission.VIEW_BUSINESS,
            SecurityPermission.VIEW_BOARD,
        },

        SecurityRole.FAMILY_MEMBER: {
            SecurityPermission.VIEW_MAHAL,
            SecurityPermission.VIEW_FAMILY,
            SecurityPermission.VIEW_ESTATE,
        },

        SecurityRole.STAFF: {
            SecurityPermission.VIEW_MAHAL,
            SecurityPermission.VIEW_ESTATE,
        },

        SecurityRole.REVIEWER: {
            SecurityPermission.VIEW_VERIFICATION,
            SecurityPermission.MANAGE_VERIFICATION,
            SecurityPermission.VIEW_MODERATION,
            SecurityPermission.MANAGE_MODERATION,
            SecurityPermission.VIEW_AUDIT,
        },

        SecurityRole.CREATOR: {
            SecurityPermission.VIEW_MAHAL,
        },

        SecurityRole.USER: {
            SecurityPermission.VIEW_MAHAL,
        },
    }

    def __init__(
        self,
        policy: Optional[SecurityPolicy] = None,
    ) -> None:
        self.policy = policy or SecurityPolicy()

        self._principals: Dict[str, SecurityPrincipal] = {}
        self._audit_events: Dict[str, SecurityAuditEvent] = {}

    # =========================================================
    # PRINCIPALS
    # =========================================================

    def register_principal(
        self,
        principal: SecurityPrincipal,
    ) -> SecurityPrincipal:
        """Register a security principal."""

        if principal.principal_id in self._principals:
            raise ValueError(
                "Security principal already exists."
            )

        self._principals[principal.principal_id] = principal

        return principal

    def get_principal(
        self,
        principal_id: str,
    ) -> Optional[SecurityPrincipal]:
        """Get a security principal."""

        return self._principals.get(principal_id)

    def list_principals(self) -> List[SecurityPrincipal]:
        """List all registered principals."""

        return list(self._principals.values())

    def assign_role(
        self,
        principal_id: str,
        role: SecurityRole,
    ) -> SecurityPrincipal:
        """Assign a role to a principal."""

        principal = self._require_principal(
            principal_id
        )

        principal.roles.add(role)
        principal.updated_at = _utc_now()

        return principal

    def remove_role(
        self,
        principal_id: str,
        role: SecurityRole,
    ) -> SecurityPrincipal:
        """Remove a role from a principal."""

        principal = self._require_principal(
            principal_id
        )

        principal.roles.discard(role)
        principal.updated_at = _utc_now()

        return principal

    # =========================================================
    # PERMISSIONS
    # =========================================================

    def permissions_for_role(
        self,
        role: SecurityRole,
    ) -> Set[SecurityPermission]:
        """Return permissions associated with a role."""

        return set(
            self.ROLE_PERMISSIONS.get(
                role,
                set(),
            )
        )

    def permissions_for_principal(
        self,
        principal_id: str,
    ) -> Set[SecurityPermission]:
        """Calculate effective permissions for a principal."""

        principal = self._require_principal(
            principal_id
        )

        permissions: Set[SecurityPermission] = set()

        for role in principal.roles:
            permissions.update(
                self.permissions_for_role(role)
            )

        return permissions

    def has_permission(
        self,
        principal_id: str,
        permission: SecurityPermission,
    ) -> bool:
        """Check whether a principal has a permission."""

        decision = self.authorize(
            principal_id,
            permission,
        )

        return decision == SecurityDecision.ALLOW

    # =========================================================
    # AUTHORIZATION
    # =========================================================

    def authorize(
        self,
        principal_id: str,
        permission: SecurityPermission,
        resource_type: str = "unknown",
        resource_id: Optional[str] = None,
    ) -> SecurityDecision:
        """Authorize an operation."""

        principal = self.get_principal(
            principal_id
        )

        if principal is None:
            return self._record_decision(
                principal_id=principal_id,
                permission=permission,
                resource_type=resource_type,
                resource_id=resource_id,
                decision=SecurityDecision.DENY,
                reason="Principal not found.",
            )

        if (
            self.policy.deny_inactive_principals
            and not principal.active
        ):
            return self._record_decision(
                principal_id=principal_id,
                permission=permission,
                resource_type=resource_type,
                resource_id=resource_id,
                decision=SecurityDecision.DENY,
                reason="Principal is inactive.",
            )

        permissions = self.permissions_for_principal(
            principal_id
        )

        if permission not in permissions:
            return self._record_decision(
                principal_id=principal_id,
                permission=permission,
                resource_type=resource_type,
                resource_id=resource_id,
                decision=SecurityDecision.DENY,
                reason="Permission not granted.",
            )

        return self._record_decision(
            principal_id=principal_id,
            permission=permission,
            resource_type=resource_type,
            resource_id=resource_id,
            decision=SecurityDecision.ALLOW,
            reason="Permission granted.",
        )

    # =========================================================
    # PRINCIPAL STATE
    # =========================================================

    def activate(
        self,
        principal_id: str,
    ) -> SecurityPrincipal:
        """Activate a principal."""

        principal = self._require_principal(
            principal_id
        )

        principal.active = True
        principal.updated_at = _utc_now()

        return principal

    def deactivate(
        self,
        principal_id: str,
    ) -> SecurityPrincipal:
        """Deactivate a principal."""

        principal = self._require_principal(
            principal_id
        )

        principal.active = False
        principal.updated_at = _utc_now()

        return principal

    # =========================================================
    # AUDIT
    # =========================================================

    def create_audit_event(
        self,
        event: SecurityAuditEvent,
    ) -> SecurityAuditEvent:
        """Store a security audit event."""

        if event.event_id in self._audit_events:
            raise ValueError(
                "Audit event already exists."
            )

        self._audit_events[event.event_id] = event

        return event

    def get_audit_event(
        self,
        event_id: str,
    ) -> Optional[SecurityAuditEvent]:
        """Get an audit event."""

        return self._audit_events.get(event_id)

    def list_audit_events(
        self,
        principal_id: Optional[str] = None,
        decision: Optional[SecurityDecision] = None,
    ) -> List[SecurityAuditEvent]:
        """List audit events with optional filters."""

        events = list(
            self._audit_events.values()
        )

        if principal_id is not None:
            events = [
                event
                for event in events
                if event.principal_id == principal_id
            ]

        if decision is not None:
            events = [
                event
                for event in events
                if event.decision == decision
            ]

        return events

    # =========================================================
    # POLICY
    # =========================================================

    def policy_status(self) -> dict:
        """Return active security policy."""

        return {
            "deny_inactive_principals": (
                self.policy.deny_inactive_principals
            ),
            "audit_access_decisions": (
                self.policy.audit_access_decisions
            ),
            "least_privilege_required": (
                self.policy.least_privilege_required
            ),
        }

    # =========================================================
    # STATUS
    # =========================================================

    def status(self) -> dict:
        """Return safe security runtime status."""

        return {
            "service": "MUKTI_MAHAL_SECURITY",
            "principals": len(self._principals),
            "audit_events": len(self._audit_events),
            "policy": self.policy_status(),
        }

    # =========================================================
    # INTERNAL
    # =========================================================

    def _require_principal(
        self,
        principal_id: str,
    ) -> SecurityPrincipal:
        """Return a principal or raise a clear error."""

        principal = self.get_principal(
            principal_id
        )

        if principal is None:
            raise ValueError(
                "Security principal not found."
            )

        return principal

    def _record_decision(
        self,
        principal_id: str,
        permission: SecurityPermission,
        resource_type: str,
        resource_id: Optional[str],
        decision: SecurityDecision,
        reason: str,
    ) -> SecurityDecision:
        """Record an authorization decision when auditing is enabled."""

        if self.policy.audit_access_decisions:
            event_id = (
                f"auth_{len(self._audit_events) + 1}"
            )

            event = SecurityAuditEvent(
                event_id=event_id,
                principal_id=principal_id,
                action=permission.value,
                resource_type=resource_type,
                resource_id=resource_id,
                decision=decision,
                reason=reason,
            )

            self._audit_events[event_id] = event

        return decision


__all__ = [
    "SecurityRole",
    "SecurityPermission",
    "SecurityDecision",
    "SecurityPrincipal",
    "SecurityAuditEvent",
    "SecurityPolicy",
    "MuktiMahalSecurity",
]
