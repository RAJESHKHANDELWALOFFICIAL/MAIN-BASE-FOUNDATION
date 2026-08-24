"""MAIN BASE FOUNDATION authentication manager."""

from typing import Dict

from .models import Credential


class AuthenticationManager:
    """Manage authentication credential references."""

    def __init__(self):
        self.credentials: Dict[str, Credential] = {}

    def register(
        self,
        credential_id: str,
        owner_id: str,
        credential_type: str,
        provider_id: str | None = None,
    ) -> dict:
        """Register a credential reference."""

        if credential_id in self.credentials:
            return {
                "success": False,
                "error": "CREDENTIAL_ID_ALREADY_EXISTS",
                "credential_id": credential_id,
            }

        credential = Credential(
            credential_id=credential_id,
            owner_id=owner_id,
            credential_type=credential_type,
            provider_id=provider_id,
        )

        self.credentials[credential_id] = credential

        return {
            "success": True,
            "credential": credential.__dict__,
        }

    def get(
        self,
        credential_id: str,
    ) -> dict:
        """Return credential metadata."""

        credential = self.credentials.get(
            credential_id
        )

        if credential is None:
            return {
                "success": False,
                "error": "CREDENTIAL_NOT_FOUND",
                "credential_id": credential_id,
            }

        return {
            "success": True,
            "credential": credential.__dict__,
        }

    def list(self) -> dict:
        """Return credential metadata."""

        return {
            "success": True,
            "count": len(self.credentials),
            "credentials": [
                credential.__dict__
                for credential in self.credentials.values()
            ],
        }

    def enable(
        self,
        credential_id: str,
    ) -> dict:
        """Enable a credential reference."""

        credential = self.credentials.get(
            credential_id
        )

        if credential is None:
            return {
                "success": False,
                "error": "CREDENTIAL_NOT_FOUND",
            }

        credential.enabled = True
        credential.status = "ACTIVE"

        return {
            "success": True,
            "credential": credential.__dict__,
        }

    def disable(
        self,
        credential_id: str,
    ) -> dict:
        """Disable a credential reference."""

        credential = self.credentials.get(
            credential_id
        )

        if credential is None:
            return {
                "success": False,
                "error": "CREDENTIAL_NOT_FOUND",
            }

        credential.enabled = False
        credential.status = "DISABLED"

        return {
            "success": True,
            "credential": credential.__dict__,
        }

    def revoke(
        self,
        credential_id: str,
    ) -> dict:
        """Revoke a credential reference."""

        credential = self.credentials.get(
            credential_id
        )

        if credential is None:
            return {
                "success": False,
                "error": "CREDENTIAL_NOT_FOUND",
            }

        credential.enabled = False
        credential.status = "REVOKED"

        return {
            "success": True,
            "credential": credential.__dict__,
        }

    def health(self) -> dict:
        """Return authentication system health."""

        active = sum(
            1
            for credential in self.credentials.values()
            if credential.status == "ACTIVE"
        )

        return {
            "system": "Authentication Manager",
            "health": "HEALTHY",
            "registered_credentials": len(
                self.credentials
            ),
            "active_credentials": active,
        }
