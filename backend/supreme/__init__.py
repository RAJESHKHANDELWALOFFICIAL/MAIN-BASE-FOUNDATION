"""
MAIN BASE FOUNDATION

SUPREME — Public Package Interface

Central public interface for the SUPREME system.

The SUPREME package exposes:
- 👑 Owner models
- 🔐 Identity and security models
- 🧩 System and module models
- 🔌 Database connection
- 🧠 SUPREME service
- 🎛️ SUPREME controller
"""

# =========================================================
# 👑 MODELS
# =========================================================

from .model import (
    SupremeOwner,
    SupremeRole,
    SupremeProfileVisibility,
    SupremeSystemType,
    SupremePermission,
    SupremeModule,
    SupremeSystem,
    SupremeControlScope,
    SupremeIdentityState,
    SupremeSystemStatus,
)


# =========================================================
# 🔌 CONNECTION
# =========================================================

from .connection import (
    SupremeConnection,
)


# =========================================================
# 🧠 SERVICE
# =========================================================

from .service import (
    SupremeService,
)


# =========================================================
# 🎛️ CONTROLLER
# =========================================================

from .controller import (
    SupremeController,
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [

    # Owner / Identity
    "SupremeOwner",
    "SupremeRole",
    "SupremeProfileVisibility",

    # System
    "SupremeSystemType",
    "SupremePermission",
    "SupremeModule",
    "SupremeSystem",
    "SupremeControlScope",
    "SupremeIdentityState",
    "SupremeSystemStatus",

    # Connection
    "SupremeConnection",

    # Service
    "SupremeService",

    # Controller
    "SupremeController",
]
