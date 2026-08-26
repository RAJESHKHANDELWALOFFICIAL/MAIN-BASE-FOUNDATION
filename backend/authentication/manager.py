"""MAIN BASE FOUNDATION authentication manager.

Authentication credential-reference management.

This module manages credential metadata and lifecycle state.
It does not store plaintext passwords, access tokens, API keys,
private keys, or other secret values.
"""

from __future__ import annotations

from threading import RLock
from typing import Dict, Optional

from .models import Credential


class AuthenticationManager:
    """Manage authentication credential references."""

    def __init__(self) -> None:
        self.credentials: Dict[str, Credential] = {}
        self._lock = RLock()

    # ------------------------------------------------------------------
    # REGISTER
    # ------------------------------------------------------------------

    def register(
        self,
        credential_id: str,
        owner_id: str,
        credential_type: str,
        provider_id: Optional[str] = None,
    ) -> dict:
        """Register a credential reference."""

        with self._lock:
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
                "credential": credential.__dict__.copy(),
            }

    # ------------------------------------------------------------------
    # GET
    # ------------------------------------------------------------------

    def get(
        self,
        credential_id: str,
    ) -> dict:
        """Return credential metadata."""

        with self._lock:
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
                "credential": credential.__dict__.copy(),
            }

    # ------------------------------------------------------------------
    # LIST
    # ------------------------------------------------------------------

    def list(self) -> dict:
        """Return credential metadata."""

        with self._lock:
            return {
                "success": True,
                "count": len(self.credentials),
                "credentials": [
                    credential.__dict__.copy()
                    for credential in self.credentials.values()
                ],
            }

    # ------------------------------------------------------------------
    # ENABLE
    # ------------------------------------------------------------------

    def enable(
        self,
        credential_id: str,
    ) -> dict:
        """Enable a credential reference."""

        with self._lock:
            credential = self.credentials.get(
                credential_id
            )

            if credential is None:
                return {
                    "success": False,
                    "error": "CREDENTIAL_NOT_FOUND",
                    "credential_id": credential_id,
                }

            if credential.status == "REVOKED":
                return {
                    "success": False,
                    "error": "CREDENTIAL_ALREADY_REVOKED",
                    "credential_id": credential_id,
                }

            credential.enabled = True
            credential.status = "ACTIVE"

            return {
                "success": True,
                "credential": credential.__dict__.copy(),
            }

    # ------------------------------------------------------------------
    # DISABLE
    # ------------------------------------------------------------------

    def disable(
        self,
        credential_id: str,
    ) -> dict:
        """Disable a credential reference."""

        with self._lock:
            credential = self.credentials.get(
                credential_id
            )

            if credential is None:
                return {
                    "success": False,
                    "error": "CREDENTIAL_NOT_FOUND",
                    "credential_id": credential_id,
                }

            if credential.status == "REVOKED":
                return {
                    "success": False,
                    "error": "CREDENTIAL_ALREADY_REVOKED",
                    "credential_id": credential_id,
                }

            credential.enabled = False
            credential.status = "DISABLED"

            return {
                "success": True,
                "credential": credential.__dict__.copy(),
            }

    # ------------------------------------------------------------------
    # REVOKE
    # ------------------------------------------------------------------

    def revoke(
        self,
        credential_id: str,
    ) -> dict:
        """Revoke a credential reference permanently."""

        with self._lock:
            credential = self.credentials.get(
                credential_id
            )

            if credential is None:
                return {
                    "success": False,
                    "error": "CREDENTIAL_NOT_FOUND",
                    "credential_id": credential_id,
                }

            credential.enabled = False
            credential.status = "REVOKED"

            return {
                "success": True,
                "credential": credential.__dict__.copy(),
            }

    # ------------------------------------------------------------------
    # HEALTH
    # ------------------------------------------------------------------

    def health(self) -> dict:
        """Return authentication system health."""

        with self._lock:
            active = sum(
                1
                for credential in self.credentials.values()
                if credential.status == "ACTIVE"
            )

            disabled = sum(
                1
                for credential in self.credentials.values()
                if credential.status == "DISABLED"
            )

            revoked = sum(
                1
                for credential in self.credentials.values()
                if credential.status == "REVOKED"
            )

            return {
                "system": "Authentication Manager",
                "health": "HEALTHY",
                "registered_credentials": len(
                    self.credentials
                ),
                "active_credentials": active,
                "disabled_credentials": disabled,
                "revoked_credentials": revoked,
            }

    # ------------------------------------------------------------------
    # STATUS
    # ------------------------------------------------------------------

    def status(self) -> dict:
        """Return authentication manager status."""

        with self._lock:
            return {
                "manager": "AuthenticationManager",
                "registered_credentials": len(
                    self.credentials
                ),
            }


__all__ = [
    "AuthenticationManager",
]
