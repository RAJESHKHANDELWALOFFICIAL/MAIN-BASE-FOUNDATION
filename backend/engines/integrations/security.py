"""MAIN BASE FOUNDATION integration security boundary."""

import hashlib
import secrets
from typing import Optional


class IntegrationSecurity:
    """Safe helpers for integration authentication metadata.

    This layer deliberately does not store provider secrets.
    """

    @staticmethod
    def generate_state() -> str:
        """Generate a cryptographically secure OAuth state value."""

        return secrets.token_urlsafe(32)

    @staticmethod
    def fingerprint(
        value: Optional[str],
    ) -> Optional[str]:
        """Return a non-reversible fingerprint for diagnostics."""

        if not value:
            return None

        return hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def redact(
        value: Optional[str],
    ) -> Optional[str]:
        """Return a safe redacted representation."""

        if not value:
            return None

        if len(value) <= 8:
            return "********"

        return (
            value[:4]
            + "..."
            + value[-4:]
        )

    @staticmethod
    def validate_provider(
        provider: str,
    ) -> str:
        """Normalize and validate a provider identifier."""

        normalized = (
            provider or ""
        ).strip().upper()

        if not normalized:
            raise ValueError(
                "Integration provider is required."
            )

        return normalized
