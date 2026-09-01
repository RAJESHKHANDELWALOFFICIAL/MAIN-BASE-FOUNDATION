"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Security

Central security boundary for the Mukti Mahal ecosystem.

Security principles:
- No plaintext passwords.
- No OTP storage.
- No raw identity documents.
- No raw payment credentials.
- No raw authentication tokens.
- Sensitive values are represented by secure references.
- Verification status is separate from authorization.
- Consent status is separate from identity verification.
- Security events must not contain secrets.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Any, Dict, Optional


class MuktiMahalSecurity:
    """Central security service for Mukti Mahal."""

    HASH_ALGORITHM = "SHA-256"

    SENSITIVE_KEYS = frozenset(
        {
            "password",
            "passwd",
            "secret",
            "client_secret",
            "access_token",
            "refresh_token",
            "api_key",
            "private_key",
            "otp",
            "one_time_password",
            "credential",
            "credentials",
            "identity_document",
            "id_document",
            "payment_token",
            "card_number",
            "cvv",
        }
    )

    def __init__(self) -> None:
        self._initialized = False

    # =========================================================
    # 🚀 INITIALIZATION
    # =========================================================

    def initialize(self) -> dict:
        """Initialize Mukti Mahal security."""

        self._initialized = True

        return {
            "service": "SUPREME_MUKTI_MAHAL_SECURITY",
            "status": "READY",
            "initialized": True,
            "plaintext_secrets_allowed": False,
            "raw_identity_documents_allowed": False,
            "raw_payment_credentials_allowed": False,
        }

    # =========================================================
    # 🔑 SECURE REFERENCE
    # =========================================================

    @staticmethod
    def generate_reference_id() -> str:
        """
        Generate a cryptographically secure non-secret
        reference identifier.
        """

        return secrets.token_urlsafe(32)

    # =========================================================
    # 🧂 NONCE
    # =========================================================

    @staticmethod
    def generate_nonce(
        size: int = 32,
    ) -> str:
        """Generate a cryptographically secure nonce."""

        if size <= 0:
            raise ValueError(
                "size must be greater than zero."
            )

        return secrets.token_urlsafe(size)

    # =========================================================
    # 🔐 FINGERPRINT
    # =========================================================

    @classmethod
    def fingerprint(
        cls,
        value: str,
    ) -> str:
        """
        Generate a one-way SHA-256 fingerprint.

        This is NOT encryption and cannot recover
        the original value.
        """

        if not isinstance(value, str):
            raise TypeError(
                "value must be a string."
            )

        return hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()

    # =========================================================
    # 🔎 VERIFY FINGERPRINT
    # =========================================================

    @classmethod
    def verify_fingerprint(
        cls,
        value: str,
        expected_fingerprint: str,
    ) -> bool:
        """Safely compare a value with its fingerprint."""

        if not isinstance(value, str):
            return False

        if not isinstance(
            expected_fingerprint,
            str,
        ):
            return False

        actual = cls.fingerprint(value)

        return hmac.compare_digest(
            actual,
            expected_fingerprint,
        )

    # =========================================================
    # 🔗 REFERENCE VALIDATION
    # =========================================================

    @staticmethod
    def validate_reference(
        reference: Optional[str],
    ) -> bool:
        """Validate a non-secret reference."""

        if not isinstance(
            reference,
            str,
        ):
            return False

        return bool(reference.strip())

    # =========================================================
    # 🚫 SENSITIVE KEY CHECK
    # =========================================================

    @classmethod
    def is_sensitive_key(
        cls,
        key: Any,
    ) -> bool:
        """Determine whether a metadata key is sensitive."""

        normalized = str(
            key
        ).strip().lower()

        return normalized in cls.SENSITIVE_KEYS

    # =========================================================
    # 🧹 METADATA SANITIZATION
    # =========================================================

    @classmethod
    def sanitize_metadata(
        cls,
        metadata: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Remove known sensitive fields.

        This is intended for safe status/log/UI output.
        """

        if not isinstance(
            metadata,
            dict,
        ):
            return {}

        return {
            key: value
            for key, value in metadata.items()
            if not cls.is_sensitive_key(key)
        }

    # =========================================================
    # 🎭 MASK IDENTIFIER
    # =========================================================

    @staticmethod
    def mask_identifier(
        value: str,
        visible: int = 4,
    ) -> str:
        """Mask an identifier for safe presentation."""

        if not isinstance(
            value,
            str,
        ):
            return ""

        value = value.strip()

        if not value:
            return ""

        if visible < 0:
            visible = 0

        if len(value) <= visible:
            return "*" * len(value)

        suffix = (
            value[-visible:]
            if visible > 0
            else ""
        )

        return (
            "*" * (
                len(value) - visible
            )
            + suffix
        )

    # =========================================================
    # 🛡️ ACCESS REQUIREMENTS
    # =========================================================

    @staticmethod
    def adult_access_requirements() -> Dict[str, bool]:
        """
        Return the security requirements for restricted
        adult ecosystem functionality.
        """

        return {
            "adult_verification_required": True,
            "identity_verification_required": True,
            "consent_required": True,
            "content_rights_required": True,
        }

    # =========================================================
    # 👥 COUPLE REQUIREMENTS
    # =========================================================

    @staticmethod
    def couple_access_requirements() -> Dict[str, bool]:
        """
        Return requirements for a couple profile.

        Every participating adult is independently verified.
        """

        return {
            "minimum_members": True,
            "independent_adult_verification": True,
            "independent_identity_verification": True,
            "independent_consent": True,
        }

    # =========================================================
    # 💰 MONETIZATION REQUIREMENTS
    # =========================================================

    @staticmethod
    def monetization_requirements() -> Dict[str, bool]:
        """Return minimum monetization requirements."""

        return {
            "verified_creator": True,
            "verified_rights": True,
            "authorized_payment_provider": True,
            "raw_payment_credentials_stored": False,
        }

    # =========================================================
    # 🌐 EXTERNAL PLATFORM REQUIREMENTS
    # =========================================================

    @staticmethod
    def external_platform_requirements() -> Dict[str, bool]:
        """
        Return requirements for an external platform
        integration.
        """

        return {
            "official_provider_authorization": True,
            "authorized_connector": True,
            "content_rights_verified": True,
            "creator_consent_verified": True,
            "raw_credentials_stored": False,
        }

    # =========================================================
    # 🔒 SECRET POLICY
    # =========================================================

    @staticmethod
    def secret_policy() -> Dict[str, bool]:
        """Return the Mukti Mahal secret-storage policy."""

        return {
            "plaintext_passwords": False,
            "plaintext_tokens": False,
            "plaintext_api_keys": False,
            "plaintext_otp": False,
            "raw_identity_documents": False,
            "raw_payment_credentials": False,
            "raw_private_keys": False,
        }

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return safe security-service status."""

        return {
            "service": (
                "SUPREME_MUKTI_MAHAL_SECURITY"
            ),
            "initialized": self._initialized,
            "hash_algorithm": self.HASH_ALGORITHM,
            "plaintext_secrets_allowed": False,
            "raw_identity_documents_allowed": False,
            "raw_payment_credentials_allowed": False,
            "secret_logging_allowed": False,
        }


__all__ = [
    "MuktiMahalSecurity",
]
