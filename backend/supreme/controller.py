"""
MAIN BASE FOUNDATION
SUPREME — Controller Layer

Central controller for the SUPREME system.

Responsibilities:
- Coordinate SUPREME service operations
- Keep controller logic separate from database logic
- Expose owner lifecycle operations
- Expose authentication operations
- Provide a single control entry point for the upper layers

Business rules remain inside SupremeService.
Database operations remain inside the service/repository layer.
"""

from typing import Any, Dict, Optional

from backend.supreme.service import SupremeService


class SupremeController:
    """
    Main controller for SUPREME.

    The controller coordinates requests and delegates
    actual business operations to SupremeService.
    """

    def __init__(
        self,
        service: Optional[SupremeService] = None,
    ) -> None:

        self.service = (
            service
            if service is not None
            else SupremeService()
        )

    # =====================================================
    # 🚀 INITIALIZATION
    # =====================================================

    def initialize(self) -> Any:
        """
        Initialize the SUPREME service.
        """

        return self.service.initialize()

    # =====================================================
    # 👑 OWNER — CREATE
    # =====================================================

    def create(self, **kwargs: Any) -> Any:
        """
        Create and persist the SUPREME owner.
        """

        owner = self.service.create_owner(
            **kwargs
        )

        self.service.save_owner(owner)

        return owner

    # =====================================================
    # 👑 OWNER — GET
    # =====================================================

    def get(self) -> Any:
        """
        Return the current SUPREME owner.
        """

        return self.service.get_owner()

    # =====================================================
    # 👑 OWNER — UPDATE
    # =====================================================

    def update(self, owner: Any) -> Any:
        """
        Update the SUPREME owner.
        """

        return self.service.update_owner(
            owner
        )

    # =====================================================
    # 👑 OWNER — DELETE
    # =====================================================

    def delete(
        self,
        supreme_id: str,
    ) -> Any:
        """
        Delete a SUPREME owner by supreme_id.
        """

        if not isinstance(
            supreme_id,
            str,
        ):
            raise TypeError(
                "supreme_id must be a string."
            )

        if not supreme_id.strip():
            raise ValueError(
                "supreme_id cannot be empty."
            )

        return self.service.delete_owner(
            supreme_id
        )

    # =====================================================
    # 👑 OWNER — LIST
    # =====================================================

    def list(self) -> Any:
        """
        Return SUPREME owner records.
        """

        return self.service.list_owner()

    # =====================================================
    # 🔎 OWNER — EXISTS
    # =====================================================

    def exists(self) -> bool:
        """
        Check whether a SUPREME owner exists.
        """

        return bool(
            self.service.owner_exists()
        )

    # =====================================================
    # 🔐 LOGIN
    # =====================================================

    def login(
        self,
        identifier: str,
    ) -> Any:
        """
        Authenticate a SUPREME owner using the
        existing service authentication contract.
        """

        if not isinstance(
            identifier,
            str,
        ):
            raise TypeError(
                "identifier must be a string."
            )

        if not identifier.strip():
            raise ValueError(
                "identifier cannot be empty."
            )

        return self.service.login(
            identifier
        )

    # =====================================================
    # 🔓 LOGOUT
    # =====================================================

    def logout(self) -> Any:
        """
        End the current SUPREME session.
        """

        return self.service.logout()

    # =====================================================
    # 🔑 PASSWORD CHANGE
    # =====================================================

    def change_password(
        self,
        supreme_id: str,
        password: str,
    ) -> Any:
        """
        Delegate password change to the service layer.

        The controller does not store passwords.
        Password hashing and credential security must
        be handled by the authentication/security layer.
        """

        if not isinstance(
            supreme_id,
            str,
        ):
            raise TypeError(
                "supreme_id must be a string."
            )

        if not supreme_id.strip():
            raise ValueError(
                "supreme_id cannot be empty."
            )

        if not isinstance(
            password,
            str,
        ):
            raise TypeError(
                "password must be a string."
            )

        if not password:
            raise ValueError(
                "password cannot be empty."
            )

        return self.service.change_password(
            supreme_id,
            password,
        )

    # =====================================================
    # 📊 STATUS
    # =====================================================

    def status(self) -> Dict[str, Any]:
        """
        Return controller-level SUPREME status.

        Uses service methods already present in the
        existing SUPREME architecture.
        """

        return {
            "controller": "SUPREME",
            "initialized": True,
            "owner_exists": self.exists(),
        }


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "SupremeController",
]
