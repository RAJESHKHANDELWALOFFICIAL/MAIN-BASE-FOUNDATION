"""
MAIN BASE FOUNDATION

Permissions — Controller Layer

Central controller for the permission system.

Responsibilities:
- Initialize permission system
- Create permissions
- Get permissions
- Update permissions
- Delete permissions
- List permissions
- Search permissions

Business and database logic remain inside
PermissionService.
"""

from typing import Any, Optional

from backend.permissions.model import Permission
from backend.permissions.service import PermissionService


# =========================================================
# 🎛️ PERMISSION CONTROLLER
# =========================================================

class PermissionController:
    """
    Main controller for permission operations.
    """

    def __init__(
        self,
        service: Optional[PermissionService] = None,
    ) -> None:

        self.service = (
            service
            if service is not None
            else PermissionService()
        )

    # =====================================================
    # 🚀 INITIALIZE
    # =====================================================

    def initialize(self) -> Any:
        """
        Initialize the permission system.
        """

        return self.service.initialize()

    # =====================================================
    # ➕ CREATE
    # =====================================================

    def create(
        self,
        permission: Permission,
    ) -> Permission:
        """
        Create and register a permission.
        """

        if not isinstance(
            permission,
            Permission,
        ):
            raise TypeError(
                "permission must be Permission."
            )

        return self.service.create_permission(
            permission
        )

    # =====================================================
    # 🔎 GET
    # =====================================================

    def get(
        self,
        permission_id: str,
    ) -> Any:
        """
        Get a permission by permission_id.
        """

        self._validate_id(
            permission_id,
            "permission_id",
        )

        return self.service.get_permission(
            permission_id
        )

    # =====================================================
    # ✏️ UPDATE
    # =====================================================

    def update(
        self,
        permission: Permission,
    ) -> Permission:
        """
        Update an existing permission.
        """

        if not isinstance(
            permission,
            Permission,
        ):
            raise TypeError(
                "permission must be Permission."
            )

        return self.service.update_permission(
            permission
        )

    # =====================================================
    # 🗑️ DELETE
    # =====================================================

    def delete(
        self,
        permission_id: str,
    ) -> None:
        """
        Delete a permission.
        """

        self._validate_id(
            permission_id,
            "permission_id",
        )

        return self.service.delete_permission(
            permission_id
        )

    # =====================================================
    # 📋 LIST
    # =====================================================

    def list(
        self,
        status: Optional[str] = None,
    ) -> Any:
        """
        List permissions.
        """

        return self.service.list_permissions(
            status=status
        )

    # =====================================================
    # 🔍 SEARCH
    # =====================================================

    def search(
        self,
        query: str,
    ) -> Any:
        """
        Search permissions.

        Delegates search logic to PermissionService.
        """

        self._validate_id(
            query,
            "query",
        )

        return self.service.search(
            query
        )

    # =====================================================
    # 🛠️ VALIDATION
    # =====================================================

    @staticmethod
    def _validate_id(
        value: str,
        field_name: str,
    ) -> None:
        """
        Validate a required string identifier.
        """

        if not isinstance(
            value,
            str,
        ):
            raise TypeError(
                f"{field_name} must be a string."
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "PermissionController",
]
