"""MAIN BASE FOUNDATION age-gate engine."""

from datetime import datetime, timezone
from typing import Dict, Optional


class AgeGateEngine:
    """Manage age verification and restricted-access state."""

    def __init__(self):
        self.engine = "Age Gate Engine"
        self.status_value = "READY"

        self.verified = False
        self.consent_given = False
        self.access_granted = False

        self.verification_method: Optional[str] = None
        self.verified_at: Optional[str] = None

    def status(self) -> Dict[str, object]:
        """Return current age-gate status."""

        return {
            "engine": self.engine,
            "status": self.status_value,
            "verified": self.verified,
            "consent_given": self.consent_given,
            "access_granted": self.access_granted,
            "verification_method": self.verification_method,
            "verified_at": self.verified_at,
        }

    def health(self) -> Dict[str, object]:
        """Return age-gate health."""

        return {
            "engine": self.engine,
            "health": "HEALTHY",
            "status": self.status_value,
        }

    def verify(
        self,
        verification_method: str,
    ) -> Dict[str, object]:
        """Record an approved age-verification result."""

        if not verification_method.strip():
            raise ValueError(
                "verification_method is required."
            )

        self.verified = True
        self.verification_method = (
            verification_method.strip()
        )
        self.verified_at = (
            datetime.now(timezone.utc).isoformat()
        )
        self.status_value = "VERIFIED"

        self._update_access()

        return self.status()

    def consent(
        self,
        accepted: bool,
    ) -> Dict[str, object]:
        """Record explicit user consent."""

        self.consent_given = bool(accepted)

        self._update_access()

        return self.status()

    def revoke(self) -> Dict[str, object]:
        """Revoke verification and restricted access."""

        self.verified = False
        self.consent_given = False
        self.access_granted = False
        self.verification_method = None
        self.verified_at = None
        self.status_value = "READY"

        return self.status()

    def can_access(self) -> bool:
        """Return whether restricted access is allowed."""

        return (
            self.verified
            and self.consent_given
            and self.access_granted
        )

    def _update_access(self) -> None:
        """Update access only after required conditions pass."""

        self.access_granted = (
            self.verified
            and self.consent_given
        )

        if self.access_granted:
            self.status_value = "ACCESS_GRANTED"
        elif self.verified:
            self.status_value = "VERIFIED_AWAITING_CONSENT"
        else:
            self.status_value = "READY"
