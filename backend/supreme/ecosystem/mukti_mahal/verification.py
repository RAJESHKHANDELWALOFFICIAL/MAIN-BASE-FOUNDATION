"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Verification

Verification and eligibility layer for the Mukti Mahal ecosystem.

Handles:
- identity verification state
- age verification state
- consent verification state
- rights/ownership verification state
- verification review workflow

Sensitive identity documents, passwords, OTPs, biometric data and
payment credentials must never be stored directly in this module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class VerificationStatus(str, Enum):
    """Verification lifecycle states."""

    NOT_STARTED = "NOT_STARTED"
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class VerificationType(str, Enum):
    """Supported verification categories."""

    IDENTITY = "IDENTITY"
    AGE = "AGE"
    CONSENT = "CONSENT"
    RIGHTS = "RIGHTS"


class VerificationReason(str, Enum):
    """Standard verification decision reasons."""

    DOCUMENT_REQUIRED = "DOCUMENT_REQUIRED"
    INFORMATION_MISMATCH = "INFORMATION_MISMATCH"
    AGE_REQUIREMENT = "AGE_REQUIREMENT"
    CONSENT_REQUIRED = "CONSENT_REQUIRED"
    RIGHTS_REQUIRED = "RIGHTS_REQUIRED"
    POLICY = "POLICY"
    OTHER = "OTHER"


@dataclass
class VerificationRecord:
    """Represents one verification case."""

    verification_id: str
    subject_id: str
    verification_type: VerificationType

    status: VerificationStatus = VerificationStatus.NOT_STARTED

    provider: Optional[str] = None
    external_reference: Optional[str] = None

    reviewer_id: Optional[str] = None
    reason: Optional[VerificationReason] = None
    review_note: str = ""

    verified_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.verification_id:
            raise ValueError("verification_id is required")

        if not self.subject_id:
            raise ValueError("subject_id is required")


@dataclass
class VerificationPolicy:
    """Platform verification requirements."""

    identity_required: bool = True
    age_verification_required: bool = True
    consent_verification_required: bool = True
    rights_verification_required: bool = True


class MuktiMahalVerification:
    """Central verification service."""

    def __init__(
        self,
        policy: Optional[VerificationPolicy] = None,
    ) -> None:
        self.policy = policy or VerificationPolicy()
        self._records: Dict[str, VerificationRecord] = {}

    # =========================================================
    # RECORD MANAGEMENT
    # =========================================================

    def create_verification(
        self,
        record: VerificationRecord,
    ) -> VerificationRecord:
        """Create a verification case."""

        if record.verification_id in self._records:
            raise ValueError(
                "Verification record already exists."
            )

        self._records[record.verification_id] = record

        return record

    def get_verification(
        self,
        verification_id: str,
    ) -> Optional[VerificationRecord]:
        """Get a verification record."""

        return self._records.get(verification_id)

    def list_verifications(
        self,
        subject_id: Optional[str] = None,
        verification_type: Optional[VerificationType] = None,
        status: Optional[VerificationStatus] = None,
    ) -> List[VerificationRecord]:
        """List verification records with optional filters."""

        records = list(self._records.values())

        if subject_id is not None:
            records = [
                record
                for record in records
                if record.subject_id == subject_id
            ]

        if verification_type is not None:
            records = [
                record
                for record in records
                if record.verification_type == verification_type
            ]

        if status is not None:
            records = [
                record
                for record in records
                if record.status == status
            ]

        return records

    # =========================================================
    # WORKFLOW
    # =========================================================

    def start_verification(
        self,
        verification_id: str,
    ) -> VerificationRecord:
        """Start a verification process."""

        record = self._require_verification(
            verification_id
        )

        if record.status not in (
            VerificationStatus.NOT_STARTED,
            VerificationStatus.REJECTED,
            VerificationStatus.EXPIRED,
        ):
            raise ValueError(
                "Verification cannot be started from its current state."
            )

        record.status = VerificationStatus.PENDING
        record.updated_at = _utc_now()

        return record

    def start_review(
        self,
        verification_id: str,
        reviewer_id: str,
    ) -> VerificationRecord:
        """Move verification into manual review."""

        if not reviewer_id:
            raise ValueError("reviewer_id is required")

        record = self._require_verification(
            verification_id
        )

        if record.status != VerificationStatus.PENDING:
            raise ValueError(
                "Only pending verification can enter review."
            )

        record.status = VerificationStatus.UNDER_REVIEW
        record.reviewer_id = reviewer_id
        record.updated_at = _utc_now()

        return record

    def verify(
        self,
        verification_id: str,
        reviewer_id: Optional[str] = None,
        note: str = "",
        expires_at: Optional[datetime] = None,
    ) -> VerificationRecord:
        """Mark a verification as verified."""

        record = self._require_verification(
            verification_id
        )

        if record.status not in (
            VerificationStatus.PENDING,
            VerificationStatus.UNDER_REVIEW,
        ):
            raise ValueError(
                "Verification cannot be approved from its current state."
            )

        if record.status == VerificationStatus.UNDER_REVIEW:
            if not reviewer_id:
                raise ValueError(
                    "reviewer_id is required for manual approval."
                )

            if record.reviewer_id != reviewer_id:
                raise ValueError(
                    "Reviewer is not assigned to this verification."
                )

        record.status = VerificationStatus.VERIFIED
        record.review_note = note
        record.verified_at = _utc_now()
        record.expires_at = expires_at
        record.updated_at = _utc_now()

        return record

    def reject(
        self,
        verification_id: str,
        reason: VerificationReason,
        note: str = "",
    ) -> VerificationRecord:
        """Reject a verification."""

        record = self._require_verification(
            verification_id
        )

        if record.status not in (
            VerificationStatus.PENDING,
            VerificationStatus.UNDER_REVIEW,
        ):
            raise ValueError(
                "Verification cannot be rejected from its current state."
            )

        record.status = VerificationStatus.REJECTED
        record.reason = reason
        record.review_note = note
        record.updated_at = _utc_now()

        return record

    def expire(
        self,
        verification_id: str,
    ) -> VerificationRecord:
        """Mark a verification as expired."""

        record = self._require_verification(
            verification_id
        )

        if record.status != VerificationStatus.VERIFIED:
            raise ValueError(
                "Only verified records can expire."
            )

        record.status = VerificationStatus.EXPIRED
        record.updated_at = _utc_now()

        return record

    # =========================================================
    # ELIGIBILITY
    # =========================================================

    def is_verified(
        self,
        subject_id: str,
        verification_type: VerificationType,
    ) -> bool:
        """Return whether a subject has a current verified record."""

        records = self.list_verifications(
            subject_id=subject_id,
            verification_type=verification_type,
            status=VerificationStatus.VERIFIED,
        )

        now = _utc_now()

        for record in records:
            if record.expires_at is None:
                return True

            if record.expires_at > now:
                return True

        return False

    def eligibility(
        self,
        subject_id: str,
    ) -> dict:
        """Return verification eligibility for a subject."""

        identity = self.is_verified(
            subject_id,
            VerificationType.IDENTITY,
        )

        age = self.is_verified(
            subject_id,
            VerificationType.AGE,
        )

        consent = self.is_verified(
            subject_id,
            VerificationType.CONSENT,
        )

        rights = self.is_verified(
            subject_id,
            VerificationType.RIGHTS,
        )

        required_checks = []

        if self.policy.identity_required:
            required_checks.append(identity)

        if self.policy.age_verification_required:
            required_checks.append(age)

        if self.policy.consent_verification_required:
            required_checks.append(consent)

        if self.policy.rights_verification_required:
            required_checks.append(rights)

        return {
            "subject_id": subject_id,
            "identity_verified": identity,
            "age_verified": age,
            "consent_verified": consent,
            "rights_verified": rights,
            "eligible": all(required_checks),
        }

    # =========================================================
    # POLICY
    # =========================================================

    def policy_status(self) -> dict:
        """Return active verification requirements."""

        return {
            "identity_required": self.policy.identity_required,
            "age_verification_required": (
                self.policy.age_verification_required
            ),
            "consent_verification_required": (
                self.policy.consent_verification_required
            ),
            "rights_verification_required": (
                self.policy.rights_verification_required
            ),
        }

    # =========================================================
    # STATUS
    # =========================================================

    def status(self) -> dict:
        """Return safe verification runtime status."""

        return {
            "service": "MUKTI_MAHAL_VERIFICATION",
            "verification_records": len(self._records),
            "policy": self.policy_status(),
        }

    # =========================================================
    # INTERNAL
    # =========================================================

    def _require_verification(
        self,
        verification_id: str,
    ) -> VerificationRecord:
        """Return a record or raise a clear error."""

        record = self.get_verification(
            verification_id
        )

        if record is None:
            raise ValueError(
                "Verification record not found."
            )

        return record


__all__ = [
    "VerificationStatus",
    "VerificationType",
    "VerificationReason",
    "VerificationRecord",
    "VerificationPolicy",
    "MuktiMahalVerification",
]
