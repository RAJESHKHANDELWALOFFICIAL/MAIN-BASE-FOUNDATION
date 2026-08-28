"""
MAIN BASE FOUNDATION
SUPREME — Core Models

Central SUPREME owner, system, module and control models.

Security principle:
- No plaintext passwords
- SUPREME profile is OWNER_ONLY
- Authentication and authorization remain separate
- External systems are managed through authorized connectors
"""

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
# 👑 SUPREME ROLE
# =========================================================

class SupremeRole(str, Enum):
    """Supported SUPREME roles."""

    SUPREME_OWNER = "SUPREME_OWNER"


# =========================================================
# 🔐 PROFILE VISIBILITY
# =========================================================

class SupremeProfileVisibility(str, Enum):
    """SUPREME profile visibility."""

    OWNER_ONLY = "OWNER_ONLY"


# =========================================================
# 🌍 SYSTEM TYPES
# =========================================================

class SupremeSystemType(str, Enum):
    """Major systems that can be registered with SUPREME."""

    CORE = "CORE"
    AI = "AI"
    SERVER = "SERVER"
    WEB = "WEB"
    APPLICATION = "APPLICATION"
    SOFTWARE = "SOFTWARE"
    DATABASE = "DATABASE"
    SECURITY = "SECURITY"
    STORAGE = "STORAGE"
    API = "API"
    LANGUAGE = "LANGUAGE"
    VAULT = "VAULT"
    MEDIA = "MEDIA"
    GAME = "GAME"
    MOVIE = "MOVIE"
    SOCIAL = "SOCIAL"
    INTEGRATION = "INTEGRATION"
    MUKTI_MAHAL = "MUKTI_MAHAL"


# =========================================================
# 🔑 PERMISSION
# =========================================================

class SupremePermission(str, Enum):
    """High-level SUPREME permissions."""

    VIEW = "VIEW"
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    MANAGE = "MANAGE"
    CONFIGURE = "CONFIGURE"
    DEPLOY = "DEPLOY"

    MANAGE_AI = "MANAGE_AI"
    MANAGE_SERVERS = "MANAGE_SERVERS"
    MANAGE_WEB = "MANAGE_WEB"
    MANAGE_APPLICATIONS = "MANAGE_APPLICATIONS"
    MANAGE_SOFTWARE = "MANAGE_SOFTWARE"

    MANAGE_DATABASE = "MANAGE_DATABASE"
    MANAGE_SECURITY = "MANAGE_SECURITY"
    MANAGE_STORAGE = "MANAGE_STORAGE"
    MANAGE_API = "MANAGE_API"

    MANAGE_LANGUAGE = "MANAGE_LANGUAGE"
    MANAGE_VAULT = "MANAGE_VAULT"

    MANAGE_MEDIA = "MANAGE_MEDIA"
    MANAGE_GAME = "MANAGE_GAME"
    MANAGE_MOVIE = "MANAGE_MOVIE"

    MANAGE_SOCIAL = "MANAGE_SOCIAL"
    MANAGE_INTEGRATIONS = "MANAGE_INTEGRATIONS"

    MANAGE_MUKTI_MAHAL = "MANAGE_MUKTI_MAHAL"


# =========================================================
# 👑 SUPREME OWNER
# =========================================================

@dataclass
class SupremeOwner:
    """
    Master SUPREME owner identity.

    IMPORTANT:
    Passwords must never be stored in plaintext here.

    Authentication credentials belong to the authentication
    and security layer.
    """

    # Database
    id: Optional[int] = None

    # Master Identity
    master_id: str = ""

    # Supreme Identity
    supreme_id: str = ""

    # Personal Information
    owner_name: str = ""
    username: str = ""
    email: str = ""
    phone: str = ""

    # ❌ Removed plaintext password field.
    #
    # password: str = ""
    #
    # Authentication must use a secure password-hashing
    # system in the authentication/security layer.

    # Access Control
    role: SupremeRole = SupremeRole.SUPREME_OWNER

    level: int = 100

    status: str = "ACTIVE"

    # Security
    two_factor_enabled: bool = False

    recovery_email: Optional[str] = None
    recovery_phone: Optional[str] = None

    # Dashboard
    dashboard_name: str = (
        "🔱 🕉️ SUPREME SHIV SHAKTI SYSTEM 🕉️ 🔱"
    )

    dashboard_theme: str = "SUPREME"

    # Profile Privacy
    profile_visibility: (
        SupremeProfileVisibility
        = SupremeProfileVisibility.OWNER_ONLY
    )

    # System
    system_version: str = "1.0.0"

    # Audit
    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.master_id.strip():
            raise ValueError(
                "master_id cannot be empty."
            )

        if not self.supreme_id.strip():
            raise ValueError(
                "supreme_id cannot be empty."
            )

        if not self.owner_name.strip():
            raise ValueError(
                "owner_name cannot be empty."
            )

        if not self.username.strip():
            raise ValueError(
                "username cannot be empty."
            )

        if self.level < 0 or self.level > 100:
            raise ValueError(
                "SUPREME owner level must be "
                "between 0 and 100."
            )

        if (
            self.profile_visibility
            != SupremeProfileVisibility.OWNER_ONLY
        ):
            raise ValueError(
                "SUPREME profile must remain "
                "OWNER_ONLY."
            )


# =========================================================
# 🧩 SUPREME MODULE
# =========================================================

@dataclass
class SupremeModule:

    module_id: str

    name: str

    system_type: SupremeSystemType

    description: str = ""

    enabled: bool = True

    version: str = "1.0.0"

    permissions: List[
        SupremePermission
    ] = field(default_factory=list)

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.module_id.strip():
            raise ValueError(
                "module_id cannot be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "module name cannot be empty."
            )


# =========================================================
# 🏗️ SUPREME SYSTEM
# =========================================================

@dataclass
class SupremeSystem:

    system_id: str

    name: str

    system_type: SupremeSystemType = (
        SupremeSystemType.CORE
    )

    version: str = "1.0.0"

    active: bool = True

    modules: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.system_id.strip():
            raise ValueError(
                "system_id cannot be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "system name cannot be empty."
            )


# =========================================================
# 🎯 CONTROL SCOPE
# =========================================================

@dataclass
class SupremeControlScope:

    system_id: str

    module_id: Optional[str] = None

    permissions: List[
        SupremePermission
    ] = field(default_factory=list)

    owner_only: bool = True

    def __post_init__(self) -> None:

        if not self.system_id.strip():
            raise ValueError(
                "system_id cannot be empty."
            )

        if not self.permissions:
            raise ValueError(
                "At least one permission is required."
            )


# =========================================================
# 🔐 IDENTITY STATE
# =========================================================

@dataclass(frozen=True)
class SupremeIdentityState:

    supreme_id: str

    authenticated: bool = False

    verified: bool = False

    two_factor_verified: bool = False

    def is_fully_verified(self) -> bool:

        return (
            bool(self.supreme_id.strip())
            and self.authenticated
            and self.verified
            and self.two_factor_verified
        )


# =========================================================
# 📊 SUPREME SYSTEM STATUS
# =========================================================

@dataclass
class SupremeSystemStatus:

    system_id: str

    active: bool = True

    healthy: bool = True

    version: str = "1.0.0"

    message: str = ""

    updated_at: str = field(
        default_factory=utc_now
    )


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "SupremeRole",
    "SupremeProfileVisibility",
    "SupremeSystemType",
    "SupremePermission",
    "SupremeOwner",
    "SupremeModule",
    "SupremeSystem",
    "SupremeControlScope",
    "SupremeIdentityState",
    "SupremeSystemStatus",
]
