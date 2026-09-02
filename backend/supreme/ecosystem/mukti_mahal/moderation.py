"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Moderation

Provides moderation and safety governance for the Mukti Mahal
ecosystem.

This module handles:
- moderation states
- content review
- user/content reports
- approval and rejection
- safety enforcement
- consent and privacy requirements

No passwords, OTPs, authentication secrets, or payment credentials
are stored here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional


def _utc_now() -> datetime:
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc)


class ModerationStatus(str, Enum):
    """Possible moderation states."""

    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FLAGGED = "FLAGGED"
    SUSPENDED = "SUSPENDED"


class ModerationReason(str, Enum):
    """Standard moderation reasons."""

    SAFETY = "SAFETY"
    PRIVACY = "PRIVACY"
    CONSENT = "CONSENT"
    AGE_VERIFICATION = "AGE_VERIFICATION"
    RIGHTS = "RIGHTS"
    POLICY = "POLICY"
    USER_REPORT = "USER_REPORT"
    OTHER = "OTHER"


@dataclass
class ModerationRecord:
    """Represents one moderation case."""

    moderation_id: str
    target_id: str
    target_type: str

    status: ModerationStatus = ModerationStatus.PENDING
    reason: Optional[ModerationReason] = None

    reviewer_id: Optional[str] = None
    review_note: str = ""

    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.moderation_id:
            raise ValueError("moderation_id is required")

        if not self.target_id:
            raise ValueError("target_id is required")

        if not self.target_type:
            raise ValueError("target_type is required")


@dataclass
class ModerationReport:
    """Represents a report submitted against a target."""

    report_id: str
    target_id: str
    target_type: str

    reason: ModerationReason
    description: str = ""

    reporter_id: Optional[str] = None

    resolved: bool = False
    resolution_note: str = ""

    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.report_id:
            raise ValueError("report_id is required")

        if not self.target_id:
            raise ValueError("target_id is required")

        if not self.target_type:
            raise ValueError("target_type is required")


@dataclass
class ModerationPolicy:
    """
    Platform-level moderation requirements.

    These defaults establish safety boundaries without storing
    sensitive personal information.
    """

    age_verification_required: bool = True
    consent_required: bool = True
    privacy_required: bool = True
    rights_verification_required: bool = True
    safety_review_required: bool = True
    user_reporting_enabled: bool = True


class MuktiMahalModeration:
    """Central moderation service for the Mukti Mahal ecosystem."""

    def __init__(
        self,
        policy: Optional[ModerationPolicy] = None,
    ) -> None:
        self.policy = policy or ModerationPolicy()

        self._records: Dict[str, ModerationRecord] = {}
        self._reports: Dict[str, ModerationReport] = {}

    # =========================================================
    # MODERATION RECORDS
    # =========================================================

    def create_moderation(
        self,
        record: ModerationRecord,
    ) -> ModerationRecord:
        """Create a moderation case."""

        if record.moderation_id in self._records:
            raise ValueError("Moderation record already exists.")

        self._records[record.moderation_id] = record
        return record

    def get_moderation(
        self,
        moderation_id: str,
    ) -> Optional[ModerationRecord]:
        """Get a moderation record."""

        return self._records.get(moderation_id)

    def list_moderations(
        self,
        status: Optional[ModerationStatus] = None,
        target_id: Optional[str] = None,
    ) -> List[ModerationRecord]:
        """List moderation records with optional filters."""

        records = list(self._records.values())

        if status is not None:
            records = [
                record
                for record in records
                if record.status == status
            ]

        if target_id is not None:
            records = [
                record
                for record in records
                if record.target_id == target_id
            ]

        return records

    # =========================================================
    # REVIEW WORKFLOW
    # =========================================================

    def start_review(
        self,
        moderation_id: str,
        reviewer_id: str,
    ) -> ModerationRecord:
        """Move a moderation case into review."""

        if not reviewer_id:
            raise ValueError("reviewer_id is required")

        record = self._require_moderation(moderation_id)

        if record.status not in (
            ModerationStatus.PENDING,
            ModerationStatus.FLAGGED,
        ):
            raise ValueError(
                "Moderation record cannot enter review."
            )

        record.status = ModerationStatus.UNDER_REVIEW
        record.reviewer_id = reviewer_id
        record.updated_at = _utc_now()

        return record

    def approve(
        self,
        moderation_id: str,
        reviewer_id: str,
        note: str = "",
    ) -> ModerationRecord:
        """Approve a moderation case."""

        record = self._require_moderation(moderation_id)

        self._require_reviewer(
            reviewer_id,
            record,
        )

        record.status = ModerationStatus.APPROVED
        record.review_note = note
        record.updated_at = _utc_now()

        return record

    def reject(
        self,
        moderation_id: str,
        reviewer_id: str,
        reason: ModerationReason,
        note: str = "",
    ) -> ModerationRecord:
        """Reject a moderation case."""

        record = self._require_moderation(moderation_id)

        self._require_reviewer(
            reviewer_id,
            record,
        )

        record.status = ModerationStatus.REJECTED
        record.reason = reason
        record.review_note = note
        record.updated_at = _utc_now()

        return record

    def suspend(
        self,
        moderation_id: str,
        reviewer_id: str,
        reason: ModerationReason,
        note: str = "",
    ) -> ModerationRecord:
        """Suspend a moderation target."""

        record = self._require_moderation(moderation_id)

        self._require_reviewer(
            reviewer_id,
            record,
        )

        record.status = ModerationStatus.SUSPENDED
        record.reason = reason
        record.review_note = note
        record.updated_at = _utc_now()

        return record

    # =========================================================
    # REPORTS
    # =========================================================

    def create_report(
        self,
        report: ModerationReport,
    ) -> ModerationReport:
        """Create a user or system moderation report."""

        if not self.policy.user_reporting_enabled:
            raise ValueError(
                "User reporting is currently disabled."
            )

        if report.report_id in self._reports:
            raise ValueError("Moderation report already exists.")

        self._reports[report.report_id] = report

        return report

    def get_report(
        self,
        report_id: str,
    ) -> Optional[ModerationReport]:
        """Get a moderation report."""

        return self._reports.get(report_id)

    def list_reports(
        self,
        target_id: Optional[str] = None,
        resolved: Optional[bool] = None,
    ) -> List[ModerationReport]:
        """List reports with optional filters."""

        reports = list(self._reports.values())

        if target_id is not None:
            reports = [
                report
                for report in reports
                if report.target_id == target_id
            ]

        if resolved is not None:
            reports = [
                report
                for report in reports
                if report.resolved == resolved
            ]

        return reports

    def resolve_report(
        self,
        report_id: str,
        resolution_note: str = "",
    ) -> ModerationReport:
        """Resolve a moderation report."""

        report = self._require_report(report_id)

        report.resolved = True
        report.resolution_note = resolution_note
        report.updated_at = _utc_now()

        return report

    # =========================================================
    # SAFETY POLICY
    # =========================================================

    def policy_status(self) -> dict:
        """Return the active moderation policy."""

        return {
            "age_verification_required": (
                self.policy.age_verification_required
            ),
            "consent_required": self.policy.consent_required,
            "privacy_required": self.policy.privacy_required,
            "rights_verification_required": (
                self.policy.rights_verification_required
            ),
            "safety_review_required": (
                self.policy.safety_review_required
            ),
            "user_reporting_enabled": (
                self.policy.user_reporting_enabled
            ),
        }

    # =========================================================
    # STATUS
    # =========================================================

    def status(self) -> dict:
        """Return safe moderation runtime status."""

        return {
            "service": "MUKTI_MAHAL_MODERATION",
            "moderation_records": len(self._records),
            "reports": len(self._reports),
            "policy": self.policy_status(),
        }

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    def _require_moderation(
        self,
        moderation_id: str,
    ) -> ModerationRecord:
        """Return a moderation record or raise an error."""

        record = self.get_moderation(moderation_id)

        if record is None:
            raise ValueError(
                "Moderation record not found."
            )

        return record

    def _require_report(
        self,
        report_id: str,
    ) -> ModerationReport:
        """Return a report or raise an error."""

        report = self.get_report(report_id)

        if report is None:
            raise ValueError(
                "Moderation report not found."
            )

        return report

    @staticmethod
    def _require_reviewer(
        reviewer_id: str,
        record: ModerationRecord,
    ) -> None:
        """Validate the reviewer for a moderation action."""

        if not reviewer_id:
            raise ValueError("reviewer_id is required")

        if record.reviewer_id != reviewer_id:
            raise ValueError(
                "Reviewer is not assigned to this moderation case."
            )


__all__ = [
    "ModerationStatus",
    "ModerationReason",
    "ModerationRecord",
    "ModerationReport",
    "ModerationPolicy",
    "MuktiMahalModeration",
]
