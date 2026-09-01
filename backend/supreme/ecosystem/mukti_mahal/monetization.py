"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Monetization Service

Central monetization layer for:

- Free content
- Paid content
- Subscriptions
- Creator monetization
- Payment-provider references
- Revenue records
- Refund references
- Monetization status

Security principles:
- Never store raw card information.
- Never store CVV.
- Never store payment passwords.
- Never store raw payment tokens.
- Payment processing remains with authorized providers.
- Only secure payment references are stored.
- Revenue records contain business metadata, not secrets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional


# =========================================================
# 🕐 TIME
# =========================================================


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(
        timezone.utc
    ).isoformat()


# =========================================================
# 💰 MONETIZATION TYPE
# =========================================================


class MuktiMahalMonetizationType(str, Enum):
    """Supported monetization models."""

    FREE = "FREE"
    ONE_TIME = "ONE_TIME"
    SUBSCRIPTION = "SUBSCRIPTION"
    TIP = "TIP"
    MEMBERSHIP = "MEMBERSHIP"
    LICENSING = "LICENSING"
    AFFILIATE = "AFFILIATE"


# =========================================================
# 📊 MONETIZATION STATUS
# =========================================================


class MuktiMahalMonetizationStatus(str, Enum):
    """Monetization lifecycle."""

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DISABLED = "DISABLED"


# =========================================================
# 💳 PAYMENT STATUS
# =========================================================


class MuktiMahalPaymentStatus(str, Enum):
    """Payment lifecycle."""

    PENDING = "PENDING"
    AUTHORIZED = "AUTHORIZED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"


# =========================================================
# 💵 PRICING REFERENCE
# =========================================================


@dataclass
class MuktiMahalPricing:
    """
    Safe pricing configuration.

    No payment credentials are stored here.
    """

    pricing_id: str

    creator_id: str

    monetization_type: MuktiMahalMonetizationType

    currency: str = "INR"

    amount: int = 0

    interval: Optional[str] = None

    active: bool = True

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.pricing_id.strip():
            raise ValueError(
                "pricing_id cannot be empty."
            )

        if not self.creator_id.strip():
            raise ValueError(
                "creator_id cannot be empty."
            )

        if not self.currency.strip():
            raise ValueError(
                "currency cannot be empty."
            )

        if self.amount < 0:
            raise ValueError(
                "amount cannot be negative."
            )


# =========================================================
# 💳 PAYMENT PROVIDER REFERENCE
# =========================================================


@dataclass
class MuktiMahalPaymentProviderReference:
    """
    Reference to an authorized payment provider.

    Raw payment credentials are never stored.
    """

    reference_id: str

    provider: str

    account_reference: str = ""

    external_customer_reference: Optional[
        str
    ] = None

    active: bool = True

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.reference_id.strip():
            raise ValueError(
                "reference_id cannot be empty."
            )

        if not self.provider.strip():
            raise ValueError(
                "provider cannot be empty."
            )


# =========================================================
# 🔗 MONETIZATION CONFIGURATION
# =========================================================


@dataclass
class MuktiMahalMonetizationConfig:
    """Creator monetization configuration."""

    monetization_id: str

    creator_id: str

    monetization_type: MuktiMahalMonetizationType

    pricing_id: Optional[str] = None

    payment_provider_reference_id: Optional[
        str
    ] = None

    status: MuktiMahalMonetizationStatus = (
        MuktiMahalMonetizationStatus.DRAFT
    )

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.monetization_id.strip():
            raise ValueError(
                "monetization_id cannot be empty."
            )

        if not self.creator_id.strip():
            raise ValueError(
                "creator_id cannot be empty."
            )


# =========================================================
# 🧾 PAYMENT RECORD
# =========================================================


@dataclass
class MuktiMahalPaymentRecord:
    """
    Business-level payment record.

    Only provider references are stored.
    """

    payment_id: str

    buyer_id: str

    creator_id: str

    payment_provider: str

    amount: int

    currency: str

    status: MuktiMahalPaymentStatus = (
        MuktiMahalPaymentStatus.PENDING
    )

    external_payment_reference: Optional[
        str
    ] = None

    content_reference: Optional[str] = None

    subscription_reference: Optional[str] = None

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.payment_id.strip():
            raise ValueError(
                "payment_id cannot be empty."
            )

        if not self.buyer_id.strip():
            raise ValueError(
                "buyer_id cannot be empty."
            )

        if not self.creator_id.strip():
            raise ValueError(
                "creator_id cannot be empty."
            )

        if not self.payment_provider.strip():
            raise ValueError(
                "payment_provider cannot be empty."
            )

        if self.amount < 0:
            raise ValueError(
                "amount cannot be negative."
            )


# =========================================================
# 📈 REVENUE RECORD
# =========================================================


@dataclass
class MuktiMahalRevenueRecord:
    """Creator revenue record."""

    revenue_id: str

    creator_id: str

    payment_id: str

    gross_amount: int

    platform_fee: int = 0

    net_amount: int = 0

    currency: str = "INR"

    created_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.revenue_id.strip():
            raise ValueError(
                "revenue_id cannot be empty."
            )

        if not self.creator_id.strip():
            raise ValueError(
                "creator_id cannot be empty."
            )

        if not self.payment_id.strip():
            raise ValueError(
                "payment_id cannot be empty."
            )

        if self.gross_amount < 0:
            raise ValueError(
                "gross_amount cannot be negative."
            )

        if self.platform_fee < 0:
            raise ValueError(
                "platform_fee cannot be negative."
            )

        if self.net_amount == 0:
            self.net_amount = (
                self.gross_amount
                - self.platform_fee
            )

        if self.net_amount < 0:
            raise ValueError(
                "net_amount cannot be negative."
            )


# =========================================================
# 💰 MONETIZATION SERVICE
# =========================================================


class MuktiMahalMonetizationService:
    """Central monetization service."""

    def __init__(self) -> None:

        self._initialized = False

        self._pricing: Dict[
            str,
            MuktiMahalPricing,
        ] = {}

        self._providers: Dict[
            str,
            MuktiMahalPaymentProviderReference,
        ] = {}

        self._configs: Dict[
            str,
            MuktiMahalMonetizationConfig,
        ] = {}

        self._payments: Dict[
            str,
            MuktiMahalPaymentRecord,
        ] = {}

        self._revenue: Dict[
            str,
            MuktiMahalRevenueRecord,
        ] = {}

    # =========================================================
    # 🚀 INITIALIZE
    # =========================================================

    def initialize(self) -> dict:
        """Initialize monetization."""

        self._initialized = True

        return {
            "service": (
                "SUPREME_MUKTI_MAHAL_MONETIZATION"
            ),
            "status": "READY",
            "initialized": True,
            "raw_payment_credentials_stored": False,
        }

    # =========================================================
    # 💵 PRICING
    # =========================================================

    def create_pricing(
        self,
        pricing: MuktiMahalPricing,
    ) -> MuktiMahalPricing:
        """Create pricing configuration."""

        if pricing.pricing_id in self._pricing:
            raise ValueError(
                "Pricing already exists."
            )

        self._pricing[
            pricing.pricing_id
        ] = pricing

        return pricing

    def get_pricing(
        self,
        pricing_id: str,
    ) -> Optional[MuktiMahalPricing]:
        """Return pricing configuration."""

        return self._pricing.get(
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

        if reference.reference_id in (
            self._providers
        ):
            raise ValueError(
                "Payment provider reference already exists."
            )

        self._providers[
            reference.reference_id
        ] = reference

        return reference

    # =========================================================
    # 🔗 MONETIZATION CONFIG
    # =========================================================

    def create_configuration(
        self,
        config: MuktiMahalMonetizationConfig,
    ) -> MuktiMahalMonetizationConfig:
        """Create creator monetization configuration."""

        if config.monetization_id in (
            self._configs
        ):
            raise ValueError(
                "Monetization configuration already exists."
            )

        if config.pricing_id is not None:
            if config.pricing_id not in (
                self._pricing
            ):
                raise ValueError(
                    "Pricing reference does not exist."
                )

        if (
            config.payment_provider_reference_id
            is not None
        ):
            if (
                config.payment_provider_reference_id
                not in self._providers
            ):
                raise ValueError(
                    "Payment provider reference does not exist."
                )

        self._configs[
            config.monetization_id
        ] = config

        return config

    # =========================================================
    # ▶️ ACTIVATE
    # =========================================================

    def activate(
        self,
        monetization_id: str,
    ) -> MuktiMahalMonetizationConfig:
        """Activate a monetization configuration."""

        config = self._configs.get(
            monetization_id
        )

        if config is None:
            raise ValueError(
                "Monetization configuration does not exist."
            )

        if (
            config.monetization_type
            != MuktiMahalMonetizationType.FREE
            and config.pricing_id is None
        ):
            raise ValueError(
                "Paid monetization requires pricing."
            )

        config.status = (
            MuktiMahalMonetizationStatus.ACTIVE
        )

        return config

    # =========================================================
    # ⏸️ PAUSE
    # =========================================================

    def pause(
        self,
        monetization_id: str,
    ) -> MuktiMahalMonetizationConfig:
        """Pause monetization."""

        config = self._configs.get(
            monetization_id
        )

        if config is None:
            raise ValueError(
                "Monetization configuration does not exist."
            )

        config.status = (
            MuktiMahalMonetizationStatus.PAUSED
        )

        return config

    # =========================================================
    # 🧾 RECORD PAYMENT
    # =========================================================

    def record_payment(
        self,
        payment: MuktiMahalPaymentRecord,
    ) -> MuktiMahalPaymentRecord:
        """Record a provider payment result."""

        if payment.payment_id in self._payments:
            raise ValueError(
                "Payment already exists."
            )

        self._payments[
            payment.payment_id
        ] = payment

        return payment

    # =========================================================
    # 📈 RECORD REVENUE
    # =========================================================

    def record_revenue(
        self,
        revenue: MuktiMahalRevenueRecord,
    ) -> MuktiMahalRevenueRecord:
        """Record creator revenue."""

        if revenue.revenue_id in self._revenue:
            raise ValueError(
                "Revenue record already exists."
            )

        payment = self._payments.get(
            revenue.payment_id
        )

        if payment is None:
            raise ValueError(
                "Payment record does not exist."
            )

        if payment.status != (
            MuktiMahalPaymentStatus.COMPLETED
        ):
            raise ValueError(
                "Revenue can only be recorded for completed payments."
            )

        self._revenue[
            revenue.revenue_id
        ] = revenue

        return revenue

    # =========================================================
    # 📊 CREATOR REVENUE
    # =========================================================

    def creator_revenue(
        self,
        creator_id: str,
    ) -> int:
        """Return total recorded net revenue."""

        return sum(
            record.net_amount
            for record in self._revenue.values()
            if record.creator_id == creator_id
        )

    # =========================================================
    # 📋 GETTERS
    # =========================================================

    def get_payment(
        self,
        payment_id: str,
    ) -> Optional[MuktiMahalPaymentRecord]:
        """Return a payment record."""

        return self._payments.get(
            payment_id
        )

    def get_configuration(
        self,
        monetization_id: str,
    ) -> Optional[
        MuktiMahalMonetizationConfig
    ]:
        """Return monetization configuration."""

        return self._configs.get(
            monetization_id
        )

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return safe monetization status."""

        return {
            "service": (
                "SUPREME_MUKTI_MAHAL_MONETIZATION"
            ),
            "initialized": self._initialized,
            "pricing_count": len(
                self._pricing
            ),
            "payment_provider_count": len(
                self._providers
            ),
            "configuration_count": len(
                self._configs
            ),
            "payment_count": len(
                self._payments
            ),
            "revenue_count": len(
                self._revenue
            ),
            "raw_payment_credentials_stored": False,
        }


__all__ = [
    "MuktiMahalMonetizationType",
    "MuktiMahalMonetizationStatus",
    "MuktiMahalPaymentStatus",
    "MuktiMahalPricing",
    "MuktiMahalPaymentProviderReference",
    "MuktiMahalMonetizationConfig",
    "MuktiMahalPaymentRecord",
    "MuktiMahalRevenueRecord",
    "MuktiMahalMonetizationService",
]
