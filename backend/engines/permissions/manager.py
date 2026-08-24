"""MAIN BASE FOUNDATION permission engine."""

from typing import Dict, List, Optional

from backend.engines.base import BaseEngine


class PermissionEngine(BaseEngine):
    """Core permission, authorization and access-control engine."""

    def __init__(self):
        super().__init__("Permission Engine")

        self.permission_status = "READY"
        self.connected = False

        # What the permission applies to.
        self.resources = [
            "ACCOUNT",
            "PROFILE",
            "ORGANIZATION",
            "BUSINESS",
            "GROUP",
            "CHANNEL",
            "PAGE",
            "COMMUNITY",
            "PROJECT",
            "DOCUMENT",
            "FILE",
            "FOLDER",
            "MEDIA",
            "MESSAGE",
            "DATABASE",
            "API",
            "SYSTEM",
        ]

        # What an authorized subject may do.
        self.actions = [
            "VIEW",
            "CREATE",
            "EDIT",
            "UPLOAD",
            "DOWNLOAD",
            "SHARE",
            "MOVE",
            "COPY",
            "PUBLISH",
            "APPROVE",
            "MANAGE",
            "EXPORT",
            "IMPORT",
            "ARCHIVE",
            "RESTORE",
            "DELETE",
        ]

        # Where the permission applies.
        self.scopes = [
            "OWN",
            "ASSIGNED",
            "TEAM",
            "DEPARTMENT",
            "ORGANIZATION",
            "SELECTED_RESOURCE",
            "PUBLIC",
            "PRIVATE",
            "GLOBAL",
        ]

        # Conditions that may restrict an otherwise valid permission.
        self.conditions = [
            "TIME_LIMIT",
            "DATE_LIMIT",
            "LOCATION_LIMIT",
            "DEVICE_LIMIT",
            "APPROVAL_REQUIRED",
            "AGE_REQUIREMENT",
            "VERIFICATION_REQUIRED",
            "ACCOUNT_STATUS_REQUIRED",
        ]

        # Permission lifecycle.
        self.statuses = [
            "DRAFT",
            "PENDING",
            "APPROVED",
            "ACTIVE",
            "SUSPENDED",
            "EXPIRED",
            "REVOKED",
            "REJECTED",
        ]

        # Stored permission records.
        self.permission_records: List[Dict[str, object]] = []

    def status(self) -> Dict[str, object]:
        """Return current permission engine status."""

        return {
            "engine": "Permission Engine",
            "status": self.permission_status,
            "connected": self.connected,
            "resources": len(self.resources),
            "actions": len(self.actions),
            "scopes": len(self.scopes),
            "conditions": len(self.conditions),
            "statuses": len(self.statuses),
            "permission_records": len(
                self.permission_records
            ),
        }

    def health(self) -> Dict[str, object]:
        """Return permission engine health."""

        return {
            "engine": "Permission Engine",
            "health": "HEALTHY",
            "status": self.permission_status,
            "connected": self.connected,
        }

    def configuration(self) -> Dict[str, object]:
        """Return safe permission configuration."""

        return {
            "engine": "Permission Engine",
            "status": self.permission_status,
            "connected": self.connected,
            "resources": self.resources,
            "actions": self.actions,
            "scopes": self.scopes,
            "conditions": self.conditions,
            "statuses": self.statuses,
        }

    def resource_types(self) -> Dict[str, object]:
        """Return supported permission resources."""

        return {
            "engine": "Permission Engine",
            "resources": self.resources,
        }

    def action_types(self) -> Dict[str, object]:
        """Return supported permission actions."""

        return {
            "engine": "Permission Engine",
            "actions": self.actions,
        }

    def scope_types(self) -> Dict[str, object]:
        """Return supported permission scopes."""

        return {
            "engine": "Permission Engine",
            "scopes": self.scopes,
        }

    def condition_types(self) -> Dict[str, object]:
        """Return supported permission conditions."""

        return {
            "engine": "Permission Engine",
            "conditions": self.conditions,
        }

    def status_types(self) -> Dict[str, object]:
        """Return supported permission lifecycle statuses."""

        return {
            "engine": "Permission Engine",
            "statuses": self.statuses,
        }

    def grant(
        self,
        permission_id: str,
        granted_to: str,
        resource: str,
        action: str,
        scope: str,
        granted_by: Optional[str] = None,
        reason: Optional[str] = None,
        purpose: Optional[str] = None,
        conditions: Optional[List[str]] = None,
        valid_from: Optional[str] = None,
        valid_until: Optional[str] = None,
    ) -> Dict[str, object]:
        """Create a permission assignment."""

        resource = resource.upper()
        action = action.upper()
        scope = scope.upper()

        requested_conditions = [
            item.upper()
            for item in (conditions or [])
        ]

        if resource not in self.resources:
            return {
                "success": False,
                "error": "INVALID_RESOURCE",
                "message": (
                    "Unsupported permission resource."
                ),
            }

        if action not in self.actions:
            return {
                "success": False,
                "error": "INVALID_ACTION",
                "message": (
                    "Unsupported permission action."
                ),
            }

        if scope not in self.scopes:
            return {
                "success": False,
                "error": "INVALID_SCOPE",
                "message": (
                    "Unsupported permission scope."
                ),
            }

        invalid_conditions = [
            condition
            for condition in requested_conditions
            if condition not in self.conditions
        ]

        if invalid_conditions:
            return {
                "success": False,
                "error": "INVALID_CONDITION",
                "invalid_conditions": invalid_conditions,
            }

        record = {
            "permission_id": permission_id,
            "granted_to": granted_to,
            "granted_by": granted_by,
            "resource": resource,
            "action": action,
            "scope": scope,
            "conditions": requested_conditions,
            "reason": reason,
            "purpose": purpose,
            "valid_from": valid_from,
            "valid_until": valid_until,
            "status": "PENDING",
            "version": 1,
        }

        self.permission_records.append(record)

        return {
            "success": True,
            "permission": record,
        }

    def list_permissions(self) -> Dict[str, object]:
        """Return all permission records."""

        return {
            "engine": "Permission Engine",
            "count": len(self.permission_records),
            "permissions": self.permission_records,
        }

    def get_permission(
        self,
        permission_id: str,
    ) -> Dict[str, object]:
        """Return one permission record."""

        for record in self.permission_records:
            if record["permission_id"] == permission_id:
                return {
                    "success": True,
                    "permission": record,
                }

        return {
            "success": False,
            "error": "PERMISSION_NOT_FOUND",
            "permission_id": permission_id,
        }

    def approve(
        self,
        permission_id: str,
        approved_by: str,
    ) -> Dict[str, object]:
        """Approve a pending permission."""

        result = self.get_permission(permission_id)

        if not result["success"]:
            return result

        permission = result["permission"]

        if permission["status"] != "PENDING":
            return {
                "success": False,
                "error": "INVALID_STATUS",
                "message": (
                    "Only PENDING permissions can be approved."
                ),
            }

        permission["status"] = "APPROVED"
        permission["approved_by"] = approved_by

        return {
            "success": True,
            "permission": permission,
        }

    def activate(
        self,
        permission_id: str,
    ) -> Dict[str, object]:
        """Activate an approved permission."""

        result = self.get_permission(permission_id)

        if not result["success"]:
            return result

        permission = result["permission"]

        if permission["status"] != "APPROVED":
            return {
                "success": False,
                "error": "INVALID_STATUS",
                "message": (
                    "Only APPROVED permissions can be activated."
                ),
            }

        permission["status"] = "ACTIVE"

        return {
            "success": True,
            "permission": permission,
        }

    def suspend(
        self,
        permission_id: str,
    ) -> Dict[str, object]:
        """Suspend an active permission."""

        result = self.get_permission(permission_id)

        if not result["success"]:
            return result

        permission = result["permission"]

        if permission["status"] != "ACTIVE":
            return {
                "success": False,
                "error": "INVALID_STATUS",
                "message": (
                    "Only ACTIVE permissions can be suspended."
                ),
            }

        permission["status"] = "SUSPENDED"

        return {
            "success": True,
            "permission": permission,
        }

    def revoke(
        self,
        permission_id: str,
        revoked_by: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> Dict[str, object]:
        """Revoke a permission."""

        result = self.get_permission(permission_id)

        if not result["success"]:
            return result

        permission = result["permission"]

        permission["status"] = "REVOKED"
        permission["revoked_by"] = revoked_by
        permission["revocation_reason"] = reason

        return {
            "success": True,
            "permission": permission,
        }

    def connect(self) -> Dict[str, object]:
        """Connect the permission engine."""

        self.connected = True
        self.permission_status = "CONNECTED"

        return self.status()

    def disconnect(self) -> Dict[str, object]:
        """Disconnect the permission engine."""

        self.connected = False
        self.permission_status = "READY"

        return self.status()
