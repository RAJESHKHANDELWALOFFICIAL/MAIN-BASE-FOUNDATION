"""
MAIN BASE FOUNDATION
Security and Access Control

Central authorization rules for foundation operations.
"""


class AccessDeniedError(PermissionError):
    """
    Raised when a requested operation is not permitted.
    """


class AccessController:
    """
    Controls which filesystem operations are permitted.
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

    def __init__(self):
        self._permissions: dict[str, set[str]] = {}

    def set_permissions(
        self,
        subject_id: str,
        operations: set[str],
    ) -> None:

        unknown = operations - self.ALLOWED_OPERATIONS

        if unknown:
            raise ValueError(
                f"Unknown operations: {sorted(unknown)}"
            )

        self._permissions[subject_id] = set(
            operations
        )

    def has_permission(
        self,
        subject_id: str,
        operation: str,
    ) -> bool:

        if operation not in self.ALLOWED_OPERATIONS:
            return False

        return operation in self._permissions.get(
            subject_id,
            set(),
        )

    def authorize(
        self,
        subject_id: str,
        operation: str,
    ) -> None:

        if not self.has_permission(
            subject_id,
            operation,
        ):
            raise AccessDeniedError(
                f"Operation '{operation}' is not "
                f"allowed for subject '{subject_id}'."
            )

    def is_protected_path(
        self,
        path: str,
    ) -> bool:

        normalized = path.replace(
            "\\",
            "/",
        ).strip("/")

        if not normalized:
            return False

        first_part = normalized.split(
            "/",
            maxsplit=1,
        )[0]

        return first_part in self.PROTECTED_PATHS

    def authorize_path(
        self,
        subject_id: str,
        operation: str,
        path: str,
    ) -> None:

        self.authorize(
            subject_id,
            operation,
        )

        if (
            operation in {
                "delete",
                "move",
                "rename",
            }
            and self.is_protected_path(path)
        ):
            raise AccessDeniedError(
                f"Protected path cannot be modified: "
                f"{path}"
            )


access_controller = AccessController()


__all__ = [
    "AccessDeniedError",
    "AccessController",
    "access_controller",
]
