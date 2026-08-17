"""
MAIN BASE FOUNDATION

Permissions — Authorization Service

Central authorization and permission-management service.

Responsibilities:
- Permission registration
- Permission lookup
- Permission listing
- Permission updates
- Permission deletion
- SUPREME OWNER permission grants
- SUPREME OWNER permission revocation
- System/module permission assignment
- Permission enforcement
- OWNER_ONLY enforcement

Authentication is NOT performed here.
This service assumes that identity has already been
authenticated by the authentication layer.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from backend.database.service import DatabaseService

from backend.permissions.model import (
    Permission,
    SupremeOwnerPermission,
    SystemPermission,
)


# =========================================================
# 🔐 PERMISSION SERVICE
# =========================================================

class PermissionService:
    """
    Central authorization service.
    """

    def __init__(
        self,
        database: Optional[DatabaseService] = None,
    ) -> None:

        self.database = (
            database
            if database is not None
            else DatabaseService()
        )

        self._initialized = False

    # =====================================================
    # 🚀 INITIALIZE
    # =====================================================

    def initialize(self) -> Dict[str, str]:
        """
        Initialize permission database structures.
        """

        self.database.initialize()

        # -------------------------------------------------
        # 🔐 PERMISSIONS
        # -------------------------------------------------

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS permissions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                permission_id TEXT UNIQUE NOT NULL,

                permission_name TEXT UNIQUE NOT NULL,

                display_name TEXT NOT NULL,

                description TEXT NOT NULL,

                status TEXT NOT NULL DEFAULT 'ACTIVE',

                owner_only INTEGER NOT NULL DEFAULT 0,

                scopes TEXT,

                metadata TEXT

            )
            """
        )

        # -------------------------------------------------
        # 👑 SUPREME OWNER PERMISSIONS
        # -------------------------------------------------

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS supreme_owner_permissions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                supreme_id TEXT NOT NULL,

                permission_id TEXT NOT NULL,

                granted INTEGER NOT NULL DEFAULT 1,

                owner_only INTEGER NOT NULL DEFAULT 1,

                metadata TEXT,

                UNIQUE (
                    supreme_id,
                    permission_id
                )

            )
            """
        )

        # -------------------------------------------------
        # 🧩 SYSTEM PERMISSIONS
        # -------------------------------------------------

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS system_permissions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                permission_id TEXT NOT NULL,

                system_id TEXT NOT NULL,

                module_id TEXT,

                enabled INTEGER NOT NULL DEFAULT 1,

                owner_only INTEGER NOT NULL DEFAULT 0,

                UNIQUE (
                    permission_id,
                    system_id,
                    module_id
                )

            )
            """
        )

        self._initialized = True

        return {
            "service": "permissions",
            "status": "READY",
        }

    # =====================================================
    # ➕ CREATE PERMISSION
    # =====================================================

    def create_permission(
        self,
        permission: Permission,
    ) -> Permission:
        """
        Register a new platform permission.
        """

        if not isinstance(
            permission,
            Permission,
        ):
            raise TypeError(
                "permission must be Permission."
            )

        self.database.execute(
            """
            INSERT OR REPLACE INTO permissions (

                permission_id,
                permission_name,
                display_name,
                description,
                status,
                owner_only,
                scopes,
                metadata

            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                permission.permission_id,
                permission.permission_name,
                permission.display_name,
                permission.description,
                permission.status,
                int(permission.owner_only),
                self._encode_list(
                    permission.scopes
                ),
                self._encode_dict(
                    permission.metadata
                ),
            ),
        )

        return permission

    # =====================================================
    # 🔎 GET PERMISSION
    # =====================================================

    def get_permission(
        self,
        permission_id: str,
    ) -> Any:
        """
        Get one permission by ID.
        """

        self._validate_id(
            permission_id,
            "permission_id",
        )

        return self.database.fetchone(
            """
            SELECT *
            FROM permissions
            WHERE permission_id=?
            LIMIT 1
            """,
            (
                permission_id,
            ),
        )

    # =====================================================
    # 📋 LIST PERMISSIONS
    # =====================================================

    def list_permissions(
        self,
        status: Optional[str] = None,
    ) -> Any:
        """
        List registered permissions.
        """

        if status is None:

            return self.database.fetchall(
                """
                SELECT *
                FROM permissions
                ORDER BY permission_name
                """
            )

        return self.database.fetchall(
            """
            SELECT *
            FROM permissions
            WHERE status=?
            ORDER BY permission_name
            """,
            (
                status,
            ),
        )

    # =====================================================
    # ✏️ UPDATE PERMISSION
    # =====================================================

    def update_permission(
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

        self.database.execute(
            """
            UPDATE permissions

            SET
                permission_name=?,
                display_name=?,
                description=?,
                status=?,
                owner_only=?,
                scopes=?,
                metadata=?

            WHERE permission_id=?
            """,
            (
                permission.permission_name,
                permission.display_name,
                permission.description,
                permission.status,
                int(permission.owner_only),
                self._encode_list(
                    permission.scopes
                ),
                self._encode_dict(
                    permission.metadata
                ),
                permission.permission_id,
            ),
        )

        return permission

    # =====================================================
    # 🗑️ DELETE PERMISSION
    # =====================================================

    def delete_permission(
        self,
        permission_id: str,
    ) -> None:
        """
        Delete a permission and its assignments.
        """

        self._validate_id(
            permission_id,
            "permission_id",
        )

        self.database.execute(
            """
            DELETE FROM supreme_owner_permissions
            WHERE permission_id=?
            """,
            (
                permission_id,
            ),
        )

        self.database.execute(
            """
            DELETE FROM system_permissions
            WHERE permission_id=?
            """,
            (
                permission_id,
            ),
        )

        self.database.execute(
            """
            DELETE FROM permissions
            WHERE permission_id=?
            """,
            (
                permission_id,
            ),
        )

    # =====================================================
    # 👑 GRANT TO SUPREME OWNER
    # =====================================================

    def grant_to_supreme_owner(
        self,
        assignment: SupremeOwnerPermission,
    ) -> SupremeOwnerPermission:
        """
        Grant a permission to the SUPREME OWNER.

        owner_only remains enforced for this assignment.
        """

        if not isinstance(
            assignment,
            SupremeOwnerPermission,
        ):
            raise TypeError(
                "assignment must be "
                "SupremeOwnerPermission."
            )

        self._validate_id(
            assignment.supreme_id,
            "supreme_id",
        )

        self._validate_id(
            assignment.permission_id,
            "permission_id",
        )

        self.database.execute(
            """
            INSERT OR REPLACE INTO
            supreme_owner_permissions (

                supreme_id,
                permission_id,
                granted,
                owner_only,
                metadata

            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                assignment.supreme_id,
                assignment.permission_id,
                int(assignment.granted),
                1,
                self._encode_dict(
                    assignment.metadata
                ),
            ),
        )

        return assignment

    # =====================================================
    # 🚫 REVOKE FROM SUPREME OWNER
    # =====================================================

    def revoke_from_supreme_owner(
        self,
        supreme_id: str,
        permission_id: str,
    ) -> None:
        """
        Revoke a permission from the SUPREME OWNER.
        """

        self._validate_id(
            supreme_id,
            "supreme_id",
        )

        self._validate_id(
            permission_id,
            "permission_id",
        )

        self.database.execute(
            """
            UPDATE supreme_owner_permissions

            SET granted=0

            WHERE supreme_id=?
              AND permission_id=?
            """,
            (
                supreme_id,
                permission_id,
            ),
        )

    # =====================================================
    # 🔎 CHECK SUPREME OWNER PERMISSION
    # =====================================================

    def has_supreme_owner_permission(
        self,
        supreme_id: str,
        permission_id: str,
    ) -> bool:
        """
        Determine whether the SUPREME OWNER has a
        specific permission.
        """

        self._validate_id(
            supreme_id,
            "supreme_id",
        )

        self._validate_id(
            permission_id,
            "permission_id",
        )

        row = self.database.fetchone(
            """
            SELECT
                p.status,
                p.owner_only,
                sop.granted,
                sop.owner_only AS assignment_owner_only

            FROM permissions p

            INNER JOIN supreme_owner_permissions sop

                ON p.permission_id =
                   sop.permission_id

            WHERE sop.supreme_id=?
              AND sop.permission_id=?

            LIMIT 1
            """,
            (
                supreme_id,
                permission_id,
            ),
        )

        if row is None:
            return False

        if row["status"] != "ACTIVE":
            return False

        if not row["granted"]:
            return False

        return True

    # =====================================================
    # 🔒 REQUIRE SUPREME OWNER PERMISSION
    # =====================================================

    def require_supreme_owner_permission(
        self,
        supreme_id: str,
        permission_id: str,
    ) -> None:
        """
        Enforce SUPREME OWNER authorization.

        Raises PermissionError when access is denied.
        """

        allowed = (
            self.has_supreme_owner_permission(
                supreme_id,
                permission_id,
            )
        )

        if not allowed:
            raise PermissionError(
                "SUPREME OWNER does not have "
                f"permission: {permission_id}"
            )

    # =====================================================
    # 🧩 ASSIGN SYSTEM PERMISSION
    # =====================================================

    def assign_system_permission(
        self,
        assignment: SystemPermission,
    ) -> SystemPermission:
        """
        Assign a permission to a system/module.
        """

        if not isinstance(
            assignment,
            SystemPermission,
        ):
            raise TypeError(
                "assignment must be SystemPermission."
            )

        self._validate_id(
            assignment.permission_id,
            "permission_id",
        )

        self._validate_id(
            assignment.system_id,
            "system_id",
        )

        self.database.execute(
            """
            INSERT OR REPLACE INTO
            system_permissions (

                permission_id,
                system_id,
                module_id,
                enabled,
                owner_only

            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                assignment.permission_id,
                assignment.system_id,
                assignment.module_id,
                int(assignment.enabled),
                int(assignment.owner_only),
            ),
        )

        return assignment

    # =====================================================
    # 🔎 CHECK SYSTEM PERMISSION
    # =====================================================

    def has_system_permission(
        self,
        permission_id: str,
        system_id: str,
        module_id: Optional[str] = None,
    ) -> bool:
        """
        Determine whether a permission is enabled
        for a system/module.
        """

        self._validate_id(
            permission_id,
            "permission_id",
        )

        self._validate_id(
            system_id,
            "system_id",
        )

        if module_id is None:

            row = self.database.fetchone(
                """
                SELECT enabled
                FROM system_permissions
                WHERE permission_id=?
                  AND system_id=?
                  AND (
                      module_id IS NULL
                      OR module_id=''
                  )
                LIMIT 1
                """,
                (
                    permission_id,
                    system_id,
                ),
            )

        else:

            row = self.database.fetchone(
                """
                SELECT enabled
                FROM system_permissions
                WHERE permission_id=?
                  AND system_id=?
                  AND module_id=?
                LIMIT 1
                """,
                (
                    permission_id,
                    system_id,
                    module_id,
                ),
            )

        return (
            row is not None
            and bool(row["enabled"])
        )

    # =====================================================
    # 🔐 OWNER-ONLY CHECK
    # =====================================================

    def is_owner_only(
        self,
        permission_id: str,
    ) -> bool:
        """
        Return whether a permission is OWNER_ONLY.
        """

        self._validate_id(
            permission_id,
            "permission_id",
        )

        row = self.database.fetchone(
            """
            SELECT owner_only
            FROM permissions
            WHERE permission_id=?
            LIMIT 1
            """,
            (
                permission_id,
            ),
        )

        if row is None:
            return False

        return bool(
            row["owner_only"]
        )

    # =====================================================
    # 👑 OWNER-ONLY ENFORCEMENT
    # =====================================================

    def require_owner_only(
        self,
        supreme_id: str,
        permission_id: str,
    ) -> None:
        """
        Enforce an OWNER_ONLY permission.

        This requires the permission to be explicitly
        granted to the supplied SUPREME owner.
        """

        if not self.is_owner_only(
            permission_id
        ):
            raise PermissionError(
                "Permission is not marked "
                "OWNER_ONLY."
            )

        self.require_supreme_owner_permission(
            supreme_id,
            permission_id,
        )

    # =====================================================
    # 📋 LIST OWNER PERMISSIONS
    # =====================================================

    def list_supreme_owner_permissions(
        self,
        supreme_id: str,
    ) -> Any:
        """
        List permissions assigned to a SUPREME owner.
        """

        self._validate_id(
            supreme_id,
            "supreme_id",
        )

        return self.database.fetchall(
            """
            SELECT
                p.permission_id,
                p.permission_name,
                p.display_name,
                p.description,
                p.status,
                p.owner_only,
                sop.granted,
                sop.owner_only AS assignment_owner_only

            FROM permissions p

            INNER JOIN supreme_owner_permissions sop

                ON p.permission_id =
                   sop.permission_id

            WHERE sop.supreme_id=?

            ORDER BY p.permission_name
            """,
            (
                supreme_id,
            ),
        )

    # =====================================================
    # 📊 STATUS
    # =====================================================

    def status(self) -> Dict[str, Any]:
        """
        Return permission service status.
        """

        return {
            "service": "permissions",
            "initialized": self._initialized,
            "authorization": "ENABLED",
            "supreme_owner_control": True,
            "owner_only_enforcement": True,
        }

    # =====================================================
    # 🛠️ VALIDATION HELPERS
    # =====================================================

    @staticmethod
    def _validate_id(
        value: str,
        field_name: str,
    ) -> None:
        """
        Validate a required identifier.
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

    @staticmethod
    def _encode_list(
        values: List[str],
    ) -> str:
        """
        Encode a list without adding a new dependency.

        JSON-like comma-separated representation is used
        only for metadata persistence.
        """

        return ",".join(
            str(value)
            for value in values
        )

    @staticmethod
    def _encode_dict(
        values: Dict[str, str],
    ) -> str:
        """
        Encode metadata as a simple key=value representation.
        """

        return ";".join(
            f"{key}={value}"
            for key, value in values.items()
        )


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "PermissionService",
]
