"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Verification Service

Central verification orchestration for:

- Adult eligibility
- Identity verification
- Consent verification
- Creator eligibility
- Couple eligibility

Security principles:
- Verification providers handle sensitive source data.
- This service stores references and statuses only.
- No identity documents are stored here.
- No passwords or OTPs are stored here.
- Adult eligibility is separate from authorization.
- Every couple member is verified independently.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .model import (
    MuktiMahalAdultVerification,
    MuktiMahalConsentRecord,
    MuktiMahalConsentStatus,
    MuktiMahalIdentityVerification,
    MuktiMahalVerificationStatus,
)


class MuktiMahalVerificationService:
    """Central verification service for Mukti Mahal."""

    def __init__(self) -> None:
        self._initialized = False

        self._adult_verifications: Dict[
            str,
            MuktiMahalAdultVerification,
        ] = {}

        self._identity_verifications: Dict[
            str,
            MuktiMahalIdentityVerification,
        ] = {}

        self._consents: Dict[
            str,
            MuktiMahalConsentRecord,
        ] = {}

    # =========================================================
    # 🚀 INITIALIZE
    # =========================================================

    def initialize(self) -> dict:
        """Initialize verification services."""

        self._initialized = True

        return {
            "service": (
                "SUPREME_MUKTI_MAHAL_VERIFICATION"
            ),
            "status": "READY",
            "initialized": True,
            "raw_documents_stored": False,
            "raw_otp_stored": False,
        }

    # =========================================================
    # 🔞 ADULT VERIFICATION
    # =========================================================

    def register_adult_verification(
        self,
        verification: MuktiMahalAdultVerification,
    ) -> MuktiMahalAdultVerification:
        """Register an adult-verification reference."""

        if (
            verification.verification_id
            in self._adult_verifications
        ):
            raise ValueError(
                "Adult verification already exists."
            )

        self._adult_verifications[
            verification.verification_id
        ] = verification

        return verification

    def get_adult_verification(
        self,
        verification_id: str,
    ) -> Optional[MuktiMahalAdultVerification]:
        """Return an adult-verification record."""

        return self._adult_verifications.get(
            verification_id
        )

    def is_verified_adult(
        self,
        subject_id: str,
    ) -> bool:
        """Check whether a subject is currently verified as an adult."""

        for verification in (
            self._adult_verifications.values()
        ):
            if (
                verification.subject_id == subject_id
                and verification.status
                == MuktiMahalVerificationStatus.VERIFIED
            ):
                return True

        return False

    # =========================================================
    # 🪪 IDENTITY VERIFICATION
    # =========================================================

    def register_identity_verification(
        self,
        verification: MuktiMahalIdentityVerification,
    ) -> MuktiMahalIdentityVerification:
        """Register an identity-verification reference."""

        if (
            verification.verification_id
            in self._identity_verifications
        ):
            raise ValueError(
                "Identity verification already exists."
            )

        self._identity_verifications[
            verification.verification_id
        ] = verification

        return verification

    def get_identity_verification(
        self,
        verification_id: str,
    ) -> Optional[MuktiMahalIdentityVerification]:
        """Return an identity-verification record."""

        return self._identity_verifications.get(
            verification_id
        )

    def is_verified_identity(
        self,
        subject_id: str,
    ) -> bool:
        """Check whether identity verification is valid."""

        for verification in (
            self._identity_verifications.values()
        ):
            if (
                verification.subject_id == subject_id
                and verification.status
                == MuktiMahalVerificationStatus.VERIFIED
            ):
                return True

        return False

    # =========================================================
    # 🤝 CONSENT
    # =========================================================

    def register_consent(
        self,
        consent: MuktiMahalConsentRecord,
    ) -> MuktiMahalConsentRecord:
        """Register an individual consent record."""

        if consent.consent_id in self._consents:
            raise ValueError(
                "Consent record already exists."
            )

        self._consents[
            consent.consent_id
        ] = consent

        return consent

    def get_consent(
        self,
        consent_id: str,
    ) -> Optional[MuktiMahalConsentRecord]:
        """Return a consent record."""

        return self._consents.get(
            consent_id
        )

    def has_active_consent(
        self,
        subject_id: str,
    ) -> bool:
        """Check whether active consent exists."""

        for consent in self._consents.values():
            if (
                consent.subject_id == subject_id
                and consent.status
                == MuktiMahalConsentStatus.GRANTED
            ):
                return True

        return False

    # =========================================================
    # 👤 INDIVIDUAL ELIGIBILITY
    # =========================================================

    def check_individual_eligibility(
        self,
        subject_id: str,
    ) -> bool:
        """
        Check minimum eligibility for protected creator
        functionality.
        """

        return (
            self.is_verified_adult(subject_id)
            and self.is_verified_identity(subject_id)
            and self.has_active_consent(subject_id)
        )

    # =========================================================
    # 👥 COUPLE ELIGIBILITY
    # =========================================================

    def check_couple_eligibility(
        self,
        member_ids: List[str],
    ) -> bool:
        """
        Check every participating member independently.

        Each member requires:
        - Adult verification
        - Identity verification
        - Active consent
        """

        if len(member_ids) < 2:
            return False

        for member_id in member_ids:

            if not self.check_individual_eligibility(
                member_id
            ):
                return False

        return True

    # =========================================================
    # 🔄 VERIFICATION STATE
    # =========================================================

    def verification_summary(
        self,
        subject_id: str,
    ) -> dict:
        """Return a safe verification summary."""

        return {
            "subject_id": subject_id,
            "adult_verified": (
                self.is_verified_adult(
                    subject_id
                )
            ),
            "identity_verified": (
                self.is_verified_identity(
                    subject_id
                )
            ),
            "consent_active": (
                self.has_active_consent(
                    subject_id
                )
            ),
            "eligible": (
                self.check_individual_eligibility(
                    subject_id
                )
            ),
        }

    # =========================================================
    # 🔒 REVOKE CONSENT
    # =========================================================

    def revoke_consent(
        self,
        consent_id: str,
    ) -> MuktiMahalConsentRecord:
        """Withdraw an existing consent record."""

        consent = self._consents.get(
            consent_id
        )

        if consent is None:
            raise ValueError(
                "Consent record does not exist."
            )

        consent.status = (
            MuktiMahalConsentStatus.WITHDRAWN
        )

        return consent

    # =========================================================
    # 🚫 REVOKE VERIFICATION
    # =========================================================

    def revoke_adult_verification(
        self,
        verification_id: str,
    ) -> MuktiMahalAdultVerification:
        """Revoke an adult-verification reference."""

        verification = (
            self._adult_verifications.get(
                verification_id
            )
        )

        if verification is None:
            raise ValueError(
                "Adult verification does not exist."
            )

        verification.status = (
            MuktiMahalVerificationStatus.REVOKED
        )

        return verification

    def revoke_identity_verification(
        self,
        verification_id: str,
    ) -> MuktiMahalIdentityVerification:
        """Revoke an identity-verification reference."""

        verification = (
            self._identity_verifications.get(
                verification_id
            )
        )

        if verification is None:
            raise ValueError(
                "Identity verification does not exist."
            )

        verification.status = (
            MuktiMahalVerificationStatus.REVOKED
        )

        return verification

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return safe verification-service status."""

        return {
            "service": (
                "SUPREME_MUKTI_MAHAL_VERIFICATION"
            ),
            "initialized": self._initialized,
            "adult_verifications": len(
                self._adult_verifications
            ),
            "identity_verifications": len(
                self._identity_verifications
            ),
            "consents": len(
                self._consents
            ),
            "raw_documents_stored": False,
            "raw_otp_stored": False,
        }


__all__ = [
    "MuktiMahalVerificationService",
]
