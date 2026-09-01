"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Moderation Service

Central content moderation lifecycle for:

- Content review
- Rights verification
- Consent verification
- Adult-content eligibility
- Publication approval
- Suspension
- Removal

Security principles:
- No raw sensitive verification data is stored here.
- No passwords, OTPs or payment credentials.
- Moderation decisions are auditable.
- Content cannot be published without required rights.
- Protected adult content requires appropriate verification.
- Consent withdrawal must be respected.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .model import (
    MuktiMahalContent,
    MuktiMahalContentRights,
    MuktiMahalContentStatus,
)
from .verification import (
    MuktiMahalVerificationService,
)


class MuktiMahalModerationService:
    """Central moderation service for Mukti Mahal."""

    def __init__(
        self,
        verification_service: Optional[
            MuktiMahalVerificationService
        ] = None,
    ) -> None:

        self.verification_service = (
            verification_service
            if verification_service is not None
            else MuktiMahalVerificationService()
        )

        self._initialized = False

        self._content: Dict[
            str,
            MuktiMahalContent,
        ] = {}

        self._rights: Dict[
            str,
            MuktiMahalContentRights,
        ] = {}

        self._decisions: List[dict] = []

    # =========================================================
    # 🚀 INITIALIZE
    # =========================================================

    def initialize(self) -> dict:
        """Initialize moderation."""

        self.verification_service.initialize()

        self._initialized = True

        return {
            "service": (
                "SUPREME_MUKTI_MAHAL_MODERATION"
            ),
            "status": "READY",
            "initialized": True,
        }

    # =========================================================
    # 🎬 REGISTER CONTENT
    # =========================================================

    def register_content(
        self,
        content: MuktiMahalContent,
    ) -> MuktiMahalContent:
        """Register content for moderation."""

        if content.content_id in self._content:
            raise ValueError(
                "Content already registered."
            )

        self._content[
            content.content_id
        ] = content

        return content

    # =========================================================
    # 🛡️ REGISTER RIGHTS
    # =========================================================

    def register_rights(
        self,
        rights: MuktiMahalContentRights,
    ) -> MuktiMahalContentRights:
        """Register content-rights information."""

        if rights.rights_id in self._rights:
            raise ValueError(
                "Rights record already registered."
            )

        if rights.content_id not in self._content:
            raise ValueError(
                "Content does not exist."
            )

        self._rights[
            rights.rights_id
        ] = rights

        return rights

    # =========================================================
    # 🔎 RIGHTS CHECK
    # =========================================================

    def has_verified_rights(
        self,
        content_id: str,
    ) -> bool:
        """Return whether verified rights exist."""

        for rights in self._rights.values():
            if (
                rights.content_id == content_id
                and rights.verified
            ):
                return True

        return False

    # =========================================================
    # 🔞 CREATOR CHECK
    # =========================================================

    def creator_is_eligible(
        self,
        creator_owner_id: str,
    ) -> bool:
        """Check creator eligibility."""

        return (
            self.verification_service
            .check_individual_eligibility(
                creator_owner_id
            )
        )

    # =========================================================
    # 🔍 SUBMIT FOR REVIEW
    # =========================================================

    def submit_for_review(
        self,
        content_id: str,
    ) -> MuktiMahalContent:
        """Move content from draft to review."""

        content = self._get_content(
            content_id
        )

        if content.status not in (
            MuktiMahalContentStatus.DRAFT,
            MuktiMahalContentStatus.REVIEW,
        ):
            raise ValueError(
                "Content cannot be submitted from its current state."
            )

        content.status = (
            MuktiMahalContentStatus.REVIEW
        )

        self._record_decision(
            content_id=content_id,
            decision="SUBMITTED_FOR_REVIEW",
            approved=False,
            reason="Content submitted for moderation.",
        )

        return content

    # =========================================================
    # ✅ APPROVE
    # =========================================================

    def approve(
        self,
        content_id: str,
        reviewer_id: str,
    ) -> MuktiMahalContent:
        """
        Approve content for publication.

        Required:
        - Existing content
        - Eligible creator
        - Verified content rights
        """

        if not reviewer_id.strip():
            raise ValueError(
                "reviewer_id cannot be empty."
            )

        content = self._get_content(
            content_id
        )

        creator_owner_id = self._creator_owner_id(
            content
        )

        if not self.creator_is_eligible(
            creator_owner_id
        ):
            self._record_decision(
                content_id=content_id,
                decision="REJECTED",
                approved=False,
                reason=(
                    "Creator verification requirements "
                    "are not satisfied."
                ),
            )

            raise PermissionError(
                "Creator verification requirements are not satisfied."
            )

        if not self.has_verified_rights(
            content_id
        ):
            self._record_decision(
                content_id=content_id,
                decision="REJECTED",
                approved=False,
                reason=(
                    "Verified content rights are required."
                ),
            )

            raise PermissionError(
                "Verified content rights are required."
            )

        content.status = (
            MuktiMahalContentStatus.APPROVED
        )

        self._record_decision(
            content_id=content_id,
            decision="APPROVED",
            approved=True,
            reason="Content approved by moderation.",
            reviewer_id=reviewer_id,
        )

        return content

    # =========================================================
    # 📤 PUBLISH
    # =========================================================

    def publish(
        self,
        content_id: str,
    ) -> MuktiMahalContent:
        """Publish previously approved content."""

        content = self._get_content(
            content_id
        )

        if content.status != (
            MuktiMahalContentStatus.APPROVED
        ):
            raise PermissionError(
                "Only approved content can be published."
            )

        content.status = (
            MuktiMahalContentStatus.PUBLISHED
        )

        self._record_decision(
            content_id=content_id,
            decision="PUBLISHED",
            approved=True,
            reason="Approved content published.",
        )

        return content

    # =========================================================
    # ⏸️ SUSPEND
    # =========================================================

    def suspend(
        self,
        content_id: str,
        reason: str,
        reviewer_id: str,
    ) -> MuktiMahalContent:
        """Suspend published or approved content."""

        if not reason.strip():
            raise ValueError(
                "reason cannot be empty."
            )

        if not reviewer_id.strip():
            raise ValueError(
                "reviewer_id cannot be empty."
            )

        content = self._get_content(
            content_id
        )

        content.status = (
            MuktiMahalContentStatus.SUSPENDED
        )

        self._record_decision(
            content_id=content_id,
            decision="SUSPENDED",
            approved=False,
            reason=reason,
            reviewer_id=reviewer_id,
        )

        return content

    # =========================================================
    # ❌ REMOVE
    # =========================================================

    def remove(
        self,
        content_id: str,
        reason: str,
        reviewer_id: str,
    ) -> MuktiMahalContent:
        """Remove content from publication."""

        if not reason.strip():
            raise ValueError(
                "reason cannot be empty."
            )

        if not reviewer_id.strip():
            raise ValueError(
                "reviewer_id cannot be empty."
            )

        content = self._get_content(
            content_id
        )

        content.status = (
            MuktiMahalContentStatus.REMOVED
        )

        self._record_decision(
            content_id=content_id,
            decision="REMOVED",
            approved=False,
            reason=reason,
            reviewer_id=reviewer_id,
        )

        return content

    # =========================================================
    # 🔎 DECISION HISTORY
    # =========================================================

    def decisions(
        self,
        content_id: Optional[str] = None,
    ) -> List[dict]:
        """Return moderation decisions."""

        if content_id is None:
            return list(self._decisions)

        return [
            decision
            for decision in self._decisions
            if decision["content_id"]
            == content_id
        ]

    # =========================================================
    # 🔧 INTERNAL HELPERS
    # =========================================================

    def _get_content(
        self,
        content_id: str,
    ) -> MuktiMahalContent:
        """Return content or raise an error."""

        content = self._content.get(
            content_id
        )

        if content is None:
            raise ValueError(
                "Content does not exist."
            )

        return content

    @staticmethod
    def _creator_owner_id(
        content: MuktiMahalContent,
    ) -> str:
        """
        Resolve creator owner reference.

        The current content model stores creator_id.
        The service therefore uses that identifier as
        the verification subject reference.
        """

        return content.creator_id

    def _record_decision(
        self,
        content_id: str,
        decision: str,
        approved: bool,
        reason: str,
        reviewer_id: str = "",
    ) -> None:
        """Record a safe moderation decision."""

        self._decisions.append(
            {
                "content_id": content_id,
                "decision": decision,
                "approved": approved,
                "reason": reason,
                "reviewer_id": reviewer_id,
            }
        )

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return safe moderation status."""

        return {
            "service": (
                "SUPREME_MUKTI_MAHAL_MODERATION"
            ),
            "initialized": self._initialized,
            "content_count": len(
                self._content
            ),
            "rights_count": len(
                self._rights
            ),
            "decision_count": len(
                self._decisions
            ),
        }


__all__ = [
    "MuktiMahalModerationService",
]
