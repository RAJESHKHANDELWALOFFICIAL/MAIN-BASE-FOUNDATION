"""
MAIN BASE FOUNDATION
Central Security and Access Control

Central authorization policy for all foundation
filesystem and management operations.
"""


class AccessDeniedError(PermissionError):
    """Raised when a foundation operation is not authorized."""

    pass


class AccessController:
    """
    Central authorization controller.

    Every protected foundation operation should pass through
    this controller before touching the filesystem or registry.
    """

    ALLOWED_OPERATIONS = {
        "read",
        "create",
        "rename",
        "move",
        "copy",
        "delete",
        "list",
        "search",
    }

    PROTECTED_PATHS = {
        ".git",
        ".github",
    }

    PROTECTED_OPERATIONS = {
        "delete",
        "move",
        "rename",
    }

    def __init__(self):
        self._permissions: dict[str, set[str]] = {}

    # ==========================================================
    # PERMISSION MANAGEMENT
    # ==========================================================

    def set_permissions(
        self,
        subject_id: str,
        operations: set[str],
    ) -> None:
        """Assign allowed operations to a subject."""

        if not subject_id:
            raise ValueError(
                "subject_id is required."
            )

        unknown = (
            set(operations)
            - self.ALLOWED_OPERATIONS
        )

        if unknown:
            raise ValueError(
                f"Unknown operations: "
                f"{sorted(unknown)}"
            )

        self._permissions[subject_id] = set(
            operations
        )

    def add_permission(
        self,
        subject_id: str,
        operation: str,
    ) -> None:
        """Add one permission to a subject."""

        self._validate_operation(operation)

        permissions = self._permissions.setdefault(
            subject_id,
            set(),
        )

        permissions.add(operation)

    def remove_permission(
        self,
        subject_id: str,
        operation: str,
    ) -> None:
        """Remove one permission from a subject."""

        self._validate_operation(operation)

        permissions = self._permissions.get(
            subject_id,
            set(),
        )

        permissions.discard(operation)

    def get_permissions(
        self,
        subject_id: str,
    ) -> set[str]:
        """Return a copy of subject permissions."""

        return set(
            self._permissions.get(
                subject_id,
                set(),
            )
        )

    # ==========================================================
    # OPERATION VALIDATION
    # ==========================================================

    def _validate_operation(
        self,
        operation: str,
    ) -> None:
        """Validate that an operation is supported."""

        if operation not in self.ALLOWED_OPERATIONS:
            raise ValueError(
                f"Unknown operation: {operation}"
            )

    def has_permission(
        self,
        subject_id: str,
        operation: str,
    ) -> bool:
        """Check whether a subject has an operation permission."""

        if operation not in self.ALLOWED_OPERATIONS:
            return False

        return operation in self._permissions.get(
            subject_id,
            set(),
        )

    # ==========================================================
    # BASIC AUTHORIZATION
    # ==========================================================

    def authorize(
        self,
        subject_id: str,
        operation: str,
    ) -> None:
        """Authorize an operation for a subject."""

        self._validate_operation(operation)

        if not subject_id:
            raise AccessDeniedError(
                "subject_id is required."
            )

        if not self.has_permission(
            subject_id,
            operation,
        ):
            raise AccessDeniedError(
                f"Operation '{operation}' is not "
                f"allowed for subject '{subject_id}'."
            )

    # ==========================================================
    # PATH SECURITY
    # ==========================================================

    def normalize_path(
        self,
        path: str,
    ) -> str:
        """Normalize a filesystem path for policy checks."""

        if path is None:
            return ""

        normalized = str(path).replace(
            "\\",
            "/",
        ).strip()

        normalized = normalized.strip("/")

        while "//" in normalized:
            normalized = normalized.replace(
                "//",
                "/",
            )

        return normalized

    def is_protected_path(
        self,
        path: str,
    ) -> bool:
        """
        Determine whether a path belongs to a protected
        foundation/system area.
        """

        normalized = self.normalize_path(
            path
        )

        if not normalized:
            return False

        parts = normalized.split("/")

        return any(
            part in self.PROTECTED_PATHS
            for part in parts
        )

    def authorize_path(
        self,
        subject_id: str,
        operation: str,
        path: str,
    ) -> None:
        """
        Authorize an operation against a specific path.
        """

        self.authorize(
            subject_id,
            operation,
        )

        normalized = self.normalize_path(
            path
        )

        if (
            operation in self.PROTECTED_OPERATIONS
            and self.is_protected_path(
                normalized
            )
        ):
            raise AccessDeniedError(
                f"Protected path cannot be "
                f"modified: {path}"
            )

    # ==========================================================
    # DESTINATION SECURITY
    # ==========================================================

    def authorize_destination(
        self,
        subject_id: str,
        operation: str,
        destination: str,
    ) -> None:
        """
        Authorize a destination path.

        This provides an explicit security boundary for
        rename, move and copy destinations.
        """

        self.authorize_path(
            subject_id=subject_id,
            operation=operation,
            path=destination,
        )

    # ==========================================================
    # POLICY INFORMATION
    # ==========================================================

    def policy(self) -> dict:
        """Return the current security policy."""

        return {
            "allowed_operations": sorted(
                self.ALLOWED_OPERATIONS
            ),
            "protected_paths": sorted(
                self.PROTECTED_PATHS
            ),
            "protected_operations": sorted(
                self.PROTECTED_OPERATIONS
            ),
        }

    def subject_policy(
        self,
        subject_id: str,
    ) -> dict:
        """Return effective policy information for a subject."""

        permissions = self.get_permissions(
            subject_id
        )

        return {
            "subject_id": subject_id,
            "permissions": sorted(
                permissions
            ),
            "authorized_operations": {
                operation: (
                    operation in permissions
                )
                for operation
                in sorted(
                    self.ALLOWED_OPERATIONS
                )
            },
        }


access_controller = AccessController()


__all__ = [
    "AccessDeniedError",
    "AccessController",
    "access_controller",
]
