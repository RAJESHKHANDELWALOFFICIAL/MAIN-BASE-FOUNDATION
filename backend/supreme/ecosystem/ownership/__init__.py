"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Ownership Public Interface

Central public interface for:
- Roles
- Permissions
- Permission scopes
- Ownership assignments
- Entity ownership
- Ownership transfers
- Access decisions
- Ownership service
- Ownership controller
"""

# =========================================================
# 👑 OWNERSHIP MODELS
# =========================================================

from .model import (
    EcosystemRole,
    OwnershipStatus,
    OwnershipAssignment,
    EntityOwnership,
    OwnershipTransfer,
    EcosystemPermission,
    PermissionScope,
    RolePermission,
    AccessDecision,
)


# =========================================================
# 🧠 OWNERSHIP SERVICE
# =========================================================

from .service import (
    OwnershipService,
)


# =========================================================
# 🎛️ OWNERSHIP CONTROLLER
# =========================================================

from .controller import (
    OwnershipController,
)


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

    # Service
    "OwnershipService",

    # Controller
    "OwnershipController",
]
