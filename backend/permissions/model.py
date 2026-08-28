"""
MAIN BASE FOUNDATION

Permissions — Core Data Models

Central permission definitions for the platform.

Permissions are independent from:
- authentication
- password management
- database implementation
- UI
- external platforms

SUPREME can use these permissions as the
authorization foundation.
"""

from dataclasses import dataclass, field
from typing import Dict, List


# =========================================================
# 🔐 PERMISSION MODEL
# =========================================================

@dataclass
class Permission:
    """
    Defines one platform permission.
    """

    permission_id: str

    permission_name: str

    display_name: str

    description: str

    status: str = "ACTIVE"

    # 🔒 Security scope
    owner_only: bool = False

    # 🌍 Systems/modules to which the permission applies
    scopes: List[str] = field(
        default_factory=list
    )

    # 📊 Additional metadata
    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        if not self.permission_id.strip():
            raise ValueError(
                "permission_id cannot be empty."
            )

        if not self.permission_name.strip():
            raise ValueError(
                "permission_name cannot be empty."
            )

        if not self.display_name.strip():
            raise ValueError(
                "display_name cannot be empty."
            )

        if not self.description.strip():
            raise ValueError(
                "description cannot be empty."
            )

        if self.status not in {
            "ACTIVE",
            "INACTIVE",
            "REVOKED",
        }:
            raise ValueError(
                "Permission status must be "
                "ACTIVE, INACTIVE or REVOKED."
            )


# =========================================================
# 👑 SUPREME OWNER PERMISSION
# =========================================================

@dataclass
class SupremeOwnerPermission:
    """
    Authorization assignment for the SUPREME OWNER.

    This does not authenticate the owner.
    It only represents authorization.
    """

    supreme_id: str

    permission_id: str

    granted: bool = True

    owner_only: bool = True

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        if not self.supreme_id.strip():
            raise ValueError(
                "supreme_id cannot be empty."
            )

        if not self.permission_id.strip():
            raise ValueError(
                "permission_id cannot be empty."
            )


# =========================================================
# 🧩 SYSTEM PERMISSION
# =========================================================

@dataclass
class SystemPermission:
    """
    Permission assigned to a specific system/module.
    """

    permission_id: str

    system_id: str

    module_id: str = ""

    enabled: bool = True

    owner_only: bool = False

    def __post_init__(self) -> None:

        if not self.permission_id.strip():
            raise ValueError(
                "permission_id cannot be empty."
            )

        if not self.system_id.strip():
            raise ValueError(
                "system_id cannot be empty."
            )


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "Permission",
    "SupremeOwnerPermission",
    "SystemPermission",
]
