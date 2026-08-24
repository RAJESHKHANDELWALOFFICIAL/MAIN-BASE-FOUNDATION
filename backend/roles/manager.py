"""MAIN BASE FOUNDATION role manager."""

from typing import Dict

from .models import Role


class RoleManager:
    """Manage organizational roles and authority assignments."""

    def __init__(self):
        self.roles: Dict[str, Role] = {}

    def create(
        self,
        role_id: str,
        role_name: str,
        organization_id: str,
        holder_id: str,
        role_category: str,
        authority_level: int,
        scope: str,
        appointment_type: str,
        description: str | None = None,
    ) -> dict:
        """Create a role assignment."""

        if role_id in self.roles:
            return {
                "success": False,
                "error": "ROLE_ID_ALREADY_EXISTS",
                "role_id": role_id,
            }

        role = Role(
            role_id=role_id,
            role_name=role_name,
            organization_id=organization_id,
            holder_id=holder_id,
            role_category=role_category,
            authority_level=authority_level,
            scope=scope,
            appointment_type=appointment_type,
            description=description,
        )

        self.roles[role_id] = role

        return {
            "success": True,
            "role": role.__dict__,
        }

    def get(
        self,
        role_id: str,
    ) -> dict:
        """Return one role."""

        role = self.roles.get(role_id)

        if role is None:
            return {
                "success": False,
                "error": "ROLE_NOT_FOUND",
                "role_id": role_id,
            }

        return {
            "success": True,
            "role": role.__dict__,
        }

    def list(self) -> dict:
        """Return all roles."""

        return {
            "success": True,
            "count": len(self.roles),
            "roles": [
                role.__dict__
                for role in self.roles.values()
            ],
        }

    def suspend(
        self,
        role_id: str,
    ) -> dict:
        """Suspend a role assignment."""

        role = self.roles.get(role_id)

        if role is None:
            return {
                "success": False,
                "error": "ROLE_NOT_FOUND",
            }

        role.status = "SUSPENDED"

        return {
            "success": True,
            "role": role.__dict__,
        }

    def revoke(
        self,
        role_id: str,
    ) -> dict:
        """Revoke a role assignment."""

        role = self.roles.get(role_id)

        if role is None:
            return {
                "success": False,
                "error": "ROLE_NOT_FOUND",
            }

        role.status = "REVOKED"

        return {
            "success": True,
            "role": role.__dict__,
        }

    def health(self) -> dict:
        """Return role system health."""

        active = sum(
            1
            for role in self.roles.values()
            if role.status == "ACTIVE"
        )

        return {
            "system": "Role Manager",
            "health": "HEALTHY",
            "registered_roles": len(self.roles),
            "active_roles": active,
        }
