"""MAIN BASE FOUNDATION secret manager."""

from typing import Dict

from .models import SecretReference


class SecretManager:
    """Manage protected secret references.

    This layer stores metadata only.
    Plaintext secret values must not be stored here.
    """

    def __init__(self):
        self.secrets: Dict[str, SecretReference] = {}

    def register(
        self,
        secret_id: str,
        owner_id: str,
        secret_type: str,
        provider_id: str | None = None,
    ) -> dict:
        """Register a protected secret reference."""

        if secret_id in self.secrets:
            return {
                "success": False,
                "error": "SECRET_ID_ALREADY_EXISTS",
                "secret_id": secret_id,
            }

        secret = SecretReference(
            secret_id=secret_id,
            owner_id=owner_id,
            secret_type=secret_type,
            provider_id=provider_id,
        )

        self.secrets[secret_id] = secret

        return {
            "success": True,
            "secret": secret.__dict__,
        }

    def get(
        self,
        secret_id: str,
    ) -> dict:
        """Return secret metadata only."""

        secret = self.secrets.get(secret_id)

        if secret is None:
            return {
                "success": False,
                "error": "SECRET_NOT_FOUND",
                "secret_id": secret_id,
            }

        return {
            "success": True,
            "secret": secret.__dict__,
        }

    def list(self) -> dict:
        """Return registered secret metadata."""

        return {
            "success": True,
            "count": len(self.secrets),
            "secrets": [
                secret.__dict__
                for secret in self.secrets.values()
            ],
        }

    def enable(
        self,
        secret_id: str,
    ) -> dict:
        """Enable a secret reference."""

        secret = self.secrets.get(secret_id)

        if secret is None:
            return {
                "success": False,
                "error": "SECRET_NOT_FOUND",
            }

        secret.enabled = True
        secret.status = "ACTIVE"

        return {
            "success": True,
            "secret": secret.__dict__,
        }

    def disable(
        self,
        secret_id: str,
    ) -> dict:
        """Disable a secret reference."""

        secret = self.secrets.get(secret_id)

        if secret is None:
            return {
                "success": False,
                "error": "SECRET_NOT_FOUND",
            }

        secret.enabled = False
        secret.status = "DISABLED"

        return {
            "success": True,
            "secret": secret.__dict__,
        }

    def revoke(
        self,
        secret_id: str,
    ) -> dict:
        """Revoke a secret reference."""

        secret = self.secrets.get(secret_id)

        if secret is None:
            return {
                "success": False,
                "error": "SECRET_NOT_FOUND",
            }

        secret.enabled = False
        secret.status = "REVOKED"

        return {
            "success": True,
            "secret": secret.__dict__,
        }

    def health(self) -> dict:
        """Return secret management health."""

        active = sum(
            1
            for secret in self.secrets.values()
            if secret.status == "ACTIVE"
        )

        return {
            "system": "Secret Manager",
            "health": "HEALTHY",
            "registered_secrets": len(self.secrets),
            "active_secrets": active,
        }
