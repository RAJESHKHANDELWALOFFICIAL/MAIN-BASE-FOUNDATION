"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Ecosystem Controller

Central public control entry point for:

- Mukti Mahal initialization
- Adult verification
- Identity verification
- Consent
- Creator eligibility
- Couple eligibility
- Content moderation
- Content rights
- Monetization
- Payment references
- Revenue
- Security status

The controller delegates business rules to
the corresponding service layers.

Security:
- No plaintext passwords.
- No OTP storage.
- No raw identity documents.
- No raw payment credentials.
- No authentication bypass.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .model import (
    MuktiMahalAdultVerification,
    MuktiMahalConsentRecord,
    MuktiMahalContent,
    MuktiMahalContentRights,
    MuktiMahalIdentityVerification,
)

from .security import (
    MuktiMahalSecurity,
)

from .verification import (
    MuktiMahalVerificationService,
)

from .moderation import (
    MuktiMahalModerationService,
)

from .monetization import (
    MuktiMahalMonetizationService,
    MuktiMahalPricing,
    MuktiMahalPaymentProviderReference,
    MuktiMahalMonetizationConfig,
    MuktiMahalPaymentRecord,
    MuktiMahalRevenueRecord,
)


class MuktiMahalController:
    """Central controller for the Mukti Mahal ecosystem."""

    def __init__(
        self,
        verification_service: Optional[
            MuktiMahalVerificationService
        ] = None,
        moderation_service: Optional[
            MuktiMahalModerationService
        ] = None,
        monetization_service: Optional[
            MuktiMahalMonetizationService
        ] = None,
        security: Optional[
            MuktiMahalSecurity
        ] = None,
    ) -> None:

        self.verification = (
            verification_service
            if verification_service is not None
            else MuktiMahalVerificationService()
        )

        self.moderation = (
            moderation_service
            if moderation_service is not None
            else MuktiMahalModerationService(
                verification_service=self.verification
            )
        )

        self.monetization = (
            monetization_service
            if monetization_service is not None
            else MuktiMahalMonetizationService()
        )

        self.security = (
            security
            if security is not None
            else MuktiMahalSecurity()
        )

        self._initialized = False

    # =========================================================
    # 🚀 INITIALIZE
    # =========================================================

    def initialize(self) -> Dict[str, Any]:
        """Initialize the complete Mukti Mahal ecosystem."""

        if not self._initialized:

            self.security.initialize()

            self.verification.initialize()

            self.moderation.initialize()

            self.monetization.initialize()

            self._initialized = True

        return self.status()

    # =========================================================
    # 🔞 ADULT VERIFICATION
    # =========================================================

    def register_adult_verification(
        self,
        verification: MuktiMahalAdultVerification,
    ) -> MuktiMahalAdultVerification:
        """Register an adult-verification result/reference."""

        self._ensure_initialized()

        return self.verification.register_adult_verification(
            verification
        )

    def get_adult_verification(
        self,
        verification_id: str,
    ) -> Optional[
        MuktiMahalAdultVerification
    ]:
        """Return an adult-verification record."""

        self._ensure_initialized()

        return self.verification.get_adult_verification(
            verification_id
        )

    def is_verified_adult(
        self,
        subject_id: str,
    ) -> bool:
        """Check adult eligibility."""

        self._ensure_initialized()

        return self.verification.is_verified_adult(
            subject_id
        )

    # =========================================================
    # 🪪 IDENTITY VERIFICATION
    # =========================================================

    def register_identity_verification(
        self,
        verification: MuktiMahalIdentityVerification,
    ) -> MuktiMahalIdentityVerification:
        """Register an identity-verification result/reference."""

        self._ensure_initialized()

        return self.verification.register_identity_verification(
            verification
        )

    def is_verified_identity(
        self,
        subject_id: str,
    ) -> bool:
        """Check identity verification."""

        self._ensure_initialized()

        return self.verification.is_verified_identity(
            subject_id
        )

    # =========================================================
    # 🤝 CONSENT
    # =========================================================

    def register_consent(
        self,
        consent: MuktiMahalConsentRecord,
    ) -> MuktiMahalConsentRecord:
        """Register an individual consent record."""

        self._ensure_initialized()

        return self.verification.register_consent(
            consent
        )

    def has_active_consent(
        self,
        subject_id: str,
    ) -> bool:
        """Check active consent."""

        self._ensure_initialized()

        return self.verification.has_active_consent(
            subject_id
        )

    def revoke_consent(
        self,
        consent_id: str,
    ) -> MuktiMahalConsentRecord:
        """Revoke consent."""

        self._ensure_initialized()

        return self.verification.revoke_consent(
            consent_id
        )

    # =========================================================
    # 👤 INDIVIDUAL ELIGIBILITY
    # =========================================================

    def check_individual_eligibility(
        self,
        subject_id: str,
    ) -> bool:
        """Check adult + identity + consent eligibility."""

        self._ensure_initialized()

        return self.verification.check_individual_eligibility(
            subject_id
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
        """

        self._ensure_initialized()

        return self.verification.check_couple_eligibility(
            member_ids
        )

    # =========================================================
    # 📋 VERIFICATION SUMMARY
    # =========================================================

    def verification_summary(
        self,
        subject_id: str,
    ) -> dict:
        """Return a safe verification summary."""

        self._ensure_initialized()

        return self.verification.verification_summary(
            subject_id
        )

    # =========================================================
    # 🎬 CONTENT
    # =========================================================

    def register_content(
        self,
        content: MuktiMahalContent,
    ) -> MuktiMahalContent:
        """Register content for moderation."""

        self._ensure_initialized()

        return self.moderation.register_content(
            content
        )

    # =========================================================
    # 🛡️ CONTENT RIGHTS
    # =========================================================

    def register_content_rights(
        self,
        rights: MuktiMahalContentRights,
    ) -> MuktiMahalContentRights:
        """Register content-rights information."""

        self._ensure_initialized()

        return self.moderation.register_rights(
            rights
        )

    def has_verified_rights(
        self,
        content_id: str,
    ) -> bool:
        """Check verified content rights."""

        self._ensure_initialized()

        return self.moderation.has_verified_rights(
            content_id
        )

    # =========================================================
    # 🔍 MODERATION
    # =========================================================

    def submit_for_review(
        self,
        content_id: str,
    ) -> MuktiMahalContent:
        """Submit content for moderation."""

        self._ensure_initialized()

        return self.moderation.submit_for_review(
            content_id
        )

    def approve_content(
        self,
        content_id: str,
        reviewer_id: str,
    ) -> MuktiMahalContent:
        """Approve content after moderation."""

        self._ensure_initialized()

        return self.moderation.approve(
            content_id=content_id,
            reviewer_id=reviewer_id,
        )

    def publish_content(
        self,
        content_id: str,
    ) -> MuktiMahalContent:
        """Publish approved content."""

        self._ensure_initialized()

        return self.moderation.publish(
            content_id
        )

    def suspend_content(
        self,
        content_id: str,
        reason: str,
        reviewer_id: str,
    ) -> MuktiMahalContent:
        """Suspend content."""

        self._ensure_initialized()

        return self.moderation.suspend(
            content_id=content_id,
            reason=reason,
            reviewer_id=reviewer_id,
        )

    def remove_content(
        self,
        content_id: str,
        reason: str,
        reviewer_id: str,
    ) -> MuktiMahalContent:
        """Remove content."""

        self._ensure_initialized()

        return self.moderation.remove(
            content_id=content_id,
            reason=reason,
            reviewer_id=reviewer_id,
        )

    def moderation_decisions(
        self,
        content_id: Optional[str] = None,
    ) -> List[dict]:
        """Return safe moderation decisions."""

        self._ensure_initialized()

        return self.moderation.decisions(
            content_id
        )

    # =========================================================
    # 💵 PRICING
    # =========================================================

    def create_pricing(
        self,
        pricing: MuktiMahalPricing,
    ) -> MuktiMahalPricing:
        """Create a free or paid pricing configuration."""

        self._ensure_initialized()

        return self.monetization.create_pricing(
            pricing
        )

    def get_pricing(
        self,
        pricing_id: str,
    ) -> Optional[MuktiMahalPricing]:
        """Return pricing."""

        self._ensure_initialized()

        return self.monetization.get_pricing(
            pricing_id
        )

    # =========================================================
    # 💳 PAYMENT PROVIDER
    # =========================================================

    def register_payment_provider(
        self,
        reference: MuktiMahalPaymentProviderReference,
    ) -> MuktiMahalPaymentProviderReference:
        """Register an authorized payment provider reference."""

        self._ensure_initialized()

        return self.monetization.register_payment_provider(
            reference
        )

    # =========================================================
    # 💰 MONETIZATION
    # =========================================================

    def create_monetization(
        self,
        config: MuktiMahalMonetizationConfig,
    ) -> MuktiMahalMonetizationConfig:
        """Create monetization configuration."""

        self._ensure_initialized()

        return self.monetization.create_configuration(
            config
        )

    def activate_monetization(
        self,
        monetization_id: str,
    ) -> MuktiMahalMonetizationConfig:
        """Activate monetization."""

        self._ensure_initialized()

        return self.monetization.activate(
            monetization_id
        )

    def pause_monetization(
        self,
        monetization_id: str,
    ) -> MuktiMahalMonetizationConfig:
        """Pause monetization."""

        self._ensure_initialized()

        return self.monetization.pause(
            monetization_id
        )

    # =========================================================
    # 🧾 PAYMENTS
    # =========================================================

    def record_payment(
        self,
        payment: MuktiMahalPaymentRecord,
    ) -> MuktiMahalPaymentRecord:
        """Record a payment-provider result."""

        self._ensure_initialized()

        return self.monetization.record_payment(
            payment
        )

    # =========================================================
    # 📈 REVENUE
    # =========================================================

    def record_revenue(
        self,
        revenue: MuktiMahalRevenueRecord,
    ) -> MuktiMahalRevenueRecord:
        """Record creator revenue."""

        self._ensure_initialized()

        return self.monetization.record_revenue(
            revenue
        )

    def creator_revenue(
        self,
        creator_id: str,
    ) -> int:
        """Return total recorded creator net revenue."""

        self._ensure_initialized()

        return self.monetization.creator_revenue(
            creator_id
        )

    # =========================================================
    # 🔐 SECURITY
    # =========================================================

    def security_policy(self) -> dict:
        """Return safe security policy."""

        self._ensure_initialized()

        return self.security.secret_policy()

    def adult_access_requirements(self) -> dict:
        """Return protected-access requirements."""

        self._ensure_initialized()

        return self.security.adult_access_requirements()

    def couple_access_requirements(self) -> dict:
        """Return couple-access requirements."""

        self._ensure_initialized()

        return self.security.couple_access_requirements()

    def monetization_requirements(self) -> dict:
        """Return monetization requirements."""

        self._ensure_initialized()

        return self.security.monetization_requirements()

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return complete safe ecosystem status."""

        return {
            "controller": (
                "SUPREME_MUKTI_MAHAL_ECOSYSTEM"
            ),
            "initialized": self._initialized,
            "security": self.security.status(),
            "verification": self.verification.status(),
            "moderation": self.moderation.status(),
            "monetization": self.monetization.status(),
        }

    # =========================================================
    # 🔧 INTERNAL
    # =========================================================

    def _ensure_initialized(self) -> None:
        """Ensure all dependent services are initialized."""

        if not self._initialized:
            self.initialize()


__all__ = [
    "MuktiMahalController",
]
