"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Monetization

Monetization and commerce layer for the Mukti Mahal ecosystem.

Handles:
- monetization plans
- subscriptions
- orders
- transactions
- refunds
- payment-provider references
- commerce status

Sensitive payment credentials, card numbers, bank details, OTPs,
passwords, API keys and payment secrets must never be stored here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional


def _utc_now() -> datetime:
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc)


class PlanStatus(str, Enum):
    """Monetization plan states."""

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ARCHIVED = "ARCHIVED"


class SubscriptionStatus(str, Enum):
    """Subscription lifecycle states."""

    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class TransactionStatus(str, Enum):
    """Transaction lifecycle states."""

    CREATED = "CREATED"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class RefundStatus(str, Enum):
    """Refund lifecycle states."""

    REQUESTED = "REQUESTED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"


class PaymentType(str, Enum):
    """Commerce transaction types."""

    SUBSCRIPTION = "SUBSCRIPTION"
    PURCHASE = "PURCHASE"
    TIP = "TIP"
    REFUND = "REFUND"


@dataclass
class MonetizationPlan:
    """Represents a purchasable monetization plan."""

    plan_id: str
    name: str
    amount: float
    currency: str = "INR"

    description: str = ""
    status: PlanStatus = PlanStatus.DRAFT

    billing_interval: str = "ONE_TIME"

    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.plan_id:
            raise ValueError("plan_id is required")

        if not self.name:
            raise ValueError("name is required")

        if self.amount < 0:
            raise ValueError("amount cannot be negative")

        if not self.currency:
            raise ValueError("currency is required")

        if not self.billing_interval:
            raise ValueError(
                "billing_interval is required"
            )


@dataclass
class Subscription:
    """Represents a user subscription."""

    subscription_id: str
    subscriber_id: str
    plan_id: str

    status: SubscriptionStatus = SubscriptionStatus.PENDING

    provider: Optional[str] = None
    external_reference: Optional[str] = None

    started_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.subscription_id:
            raise ValueError(
                "subscription_id is required"
            )

        if not self.subscriber_id:
            raise ValueError(
                "subscriber_id is required"
            )

        if not self.plan_id:
            raise ValueError(
                "plan_id is required"
            )


@dataclass
class Transaction:
    """Represents a commerce transaction."""

    transaction_id: str
    payer_id: str
    amount: float
    currency: str = "INR"

    payment_type: PaymentType = PaymentType.PURCHASE
    status: TransactionStatus = TransactionStatus.CREATED

    plan_id: Optional[str] = None
    subscription_id: Optional[str] = None

    provider: Optional[str] = None
    external_reference: Optional[str] = None

    failure_reason: str = ""

    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.transaction_id:
            raise ValueError(
                "transaction_id is required"
            )

        if not self.payer_id:
            raise ValueError(
                "payer_id is required"
            )

        if self.amount < 0:
            raise ValueError(
                "amount cannot be negative"
            )

        if not self.currency:
            raise ValueError(
                "currency is required"
            )


@dataclass
class Refund:
    """Represents a refund request."""

    refund_id: str
    transaction_id: str
    amount: float

    status: RefundStatus = RefundStatus.REQUESTED

    reason: str = ""
    provider: Optional[str] = None
    external_reference: Optional[str] = None

    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.refund_id:
            raise ValueError(
                "refund_id is required"
            )

        if not self.transaction_id:
            raise ValueError(
                "transaction_id is required"
            )

        if self.amount <= 0:
            raise ValueError(
                "refund amount must be greater than zero"
            )


class MuktiMahalMonetization:
    """Central monetization service."""

    def __init__(self) -> None:
        self._plans: Dict[str, MonetizationPlan] = {}
        self._subscriptions: Dict[str, Subscription] = {}
        self._transactions: Dict[str, Transaction] = {}
        self._refunds: Dict[str, Refund] = {}

    # =========================================================
    # PLANS
    # =========================================================

    def create_plan(
        self,
        plan: MonetizationPlan,
    ) -> MonetizationPlan:
        """Create a monetization plan."""

        if plan.plan_id in self._plans:
            raise ValueError(
                "Monetization plan already exists."
            )

        self._plans[plan.plan_id] = plan

        return plan

    def get_plan(
        self,
        plan_id: str,
    ) -> Optional[MonetizationPlan]:
        """Get a monetization plan."""

        return self._plans.get(plan_id)

    def list_plans(
        self,
        status: Optional[PlanStatus] = None,
    ) -> List[MonetizationPlan]:
        """List plans with an optional status filter."""

        plans = list(self._plans.values())

        if status is not None:
            plans = [
                plan
                for plan in plans
                if plan.status == status
            ]

        return plans

    def activate_plan(
        self,
        plan_id: str,
    ) -> MonetizationPlan:
        """Activate a monetization plan."""

        plan = self._require_plan(plan_id)

        plan.status = PlanStatus.ACTIVE
        plan.updated_at = _utc_now()

        return plan

    def deactivate_plan(
        self,
        plan_id: str,
    ) -> MonetizationPlan:
        """Deactivate a monetization plan."""

        plan = self._require_plan(plan_id)

        plan.status = PlanStatus.INACTIVE
        plan.updated_at = _utc_now()

        return plan

    # =========================================================
    # SUBSCRIPTIONS
    # =========================================================

    def create_subscription(
        self,
        subscription: Subscription,
    ) -> Subscription:
        """Create a subscription."""

        if subscription.subscription_id in self._subscriptions:
            raise ValueError(
                "Subscription already exists."
            )

        plan = self.get_plan(subscription.plan_id)

        if plan is None:
            raise ValueError(
                "Monetization plan not found."
            )

        if plan.status != PlanStatus.ACTIVE:
            raise ValueError(
                "Monetization plan is not active."
            )

        self._subscriptions[
            subscription.subscription_id
        ] = subscription

        return subscription

    def get_subscription(
        self,
        subscription_id: str,
    ) -> Optional[Subscription]:
        """Get a subscription."""

        return self._subscriptions.get(
            subscription_id
        )

    def list_subscriptions(
        self,
        subscriber_id: Optional[str] = None,
        status: Optional[SubscriptionStatus] = None,
    ) -> List[Subscription]:
        """List subscriptions with optional filters."""

        subscriptions = list(
            self._subscriptions.values()
        )

        if subscriber_id is not None:
            subscriptions = [
                subscription
                for subscription in subscriptions
                if subscription.subscriber_id
                == subscriber_id
            ]

        if status is not None:
            subscriptions = [
                subscription
                for subscription in subscriptions
                if subscription.status == status
            ]

        return subscriptions

    def activate_subscription(
        self,
        subscription_id: str,
        expires_at: Optional[datetime] = None,
    ) -> Subscription:
        """Activate a subscription."""

        subscription = self._require_subscription(
            subscription_id
        )

        subscription.status = SubscriptionStatus.ACTIVE
        subscription.started_at = (
            subscription.started_at
            or _utc_now()
        )
        subscription.expires_at = expires_at
        subscription.updated_at = _utc_now()

        return subscription

    def pause_subscription(
        self,
        subscription_id: str,
    ) -> Subscription:
        """Pause a subscription."""

        subscription = self._require_subscription(
            subscription_id
        )

        if subscription.status != SubscriptionStatus.ACTIVE:
            raise ValueError(
                "Only active subscriptions can be paused."
            )

        subscription.status = SubscriptionStatus.PAUSED
        subscription.updated_at = _utc_now()

        return subscription

    def cancel_subscription(
        self,
        subscription_id: str,
    ) -> Subscription:
        """Cancel a subscription."""

        subscription = self._require_subscription(
            subscription_id
        )

        subscription.status = SubscriptionStatus.CANCELLED
        subscription.cancelled_at = _utc_now()
        subscription.updated_at = _utc_now()

        return subscription

    # =========================================================
    # TRANSACTIONS
    # =========================================================

    def create_transaction(
        self,
        transaction: Transaction,
    ) -> Transaction:
        """Create a commerce transaction."""

        if transaction.transaction_id in self._transactions:
            raise ValueError(
                "Transaction already exists."
            )

        if transaction.plan_id is not None:
            plan = self.get_plan(
                transaction.plan_id
            )

            if plan is None:
                raise ValueError(
                    "Monetization plan not found."
                )

        self._transactions[
            transaction.transaction_id
        ] = transaction

        return transaction

    def get_transaction(
        self,
        transaction_id: str,
    ) -> Optional[Transaction]:
        """Get a transaction."""

        return self._transactions.get(
            transaction_id
        )

    def list_transactions(
        self,
        payer_id: Optional[str] = None,
        status: Optional[TransactionStatus] = None,
    ) -> List[Transaction]:
        """List transactions with optional filters."""

        transactions = list(
            self._transactions.values()
        )

        if payer_id is not None:
            transactions = [
                transaction
                for transaction in transactions
                if transaction.payer_id == payer_id
            ]

        if status is not None:
            transactions = [
                transaction
                for transaction in transactions
                if transaction.status == status
            ]

        return transactions

    def mark_transaction_pending(
        self,
        transaction_id: str,
    ) -> Transaction:
        """Move a transaction to pending."""

        transaction = self._require_transaction(
            transaction_id
        )

        transaction.status = TransactionStatus.PENDING
        transaction.updated_at = _utc_now()

        return transaction

    def mark_transaction_processing(
        self,
        transaction_id: str,
    ) -> Transaction:
        """Move a transaction to processing."""

        transaction = self._require_transaction(
            transaction_id
        )

        transaction.status = TransactionStatus.PROCESSING
        transaction.updated_at = _utc_now()

        return transaction

    def mark_transaction_success(
        self,
        transaction_id: str,
    ) -> Transaction:
        """Mark a transaction successful."""

        transaction = self._require_transaction(
            transaction_id
        )

        transaction.status = TransactionStatus.SUCCESS
        transaction.updated_at = _utc_now()

        return transaction

    def mark_transaction_failed(
        self,
        transaction_id: str,
        reason: str = "",
    ) -> Transaction:
        """Mark a transaction failed."""

        transaction = self._require_transaction(
            transaction_id
        )

        transaction.status = TransactionStatus.FAILED
        transaction.failure_reason = reason
        transaction.updated_at = _utc_now()

        return transaction

    # =========================================================
    # REFUNDS
    # =========================================================

    def create_refund(
        self,
        refund: Refund,
    ) -> Refund:
        """Create a refund request."""

        if refund.refund_id in self._refunds:
            raise ValueError(
                "Refund already exists."
            )

        transaction = self.get_transaction(
            refund.transaction_id
        )

        if transaction is None:
            raise ValueError(
                "Transaction not found."
            )

        if transaction.status != TransactionStatus.SUCCESS:
            raise ValueError(
                "Only successful transactions can be refunded."
            )

        if refund.amount > transaction.amount:
            raise ValueError(
                "Refund amount cannot exceed transaction amount."
            )

        self._refunds[
            refund.refund_id
        ] = refund

        return refund

    def get_refund(
        self,
        refund_id: str,
    ) -> Optional[Refund]:
        """Get a refund."""

        return self._refunds.get(refund_id)

    def list_refunds(
        self,
        transaction_id: Optional[str] = None,
        status: Optional[RefundStatus] = None,
    ) -> List[Refund]:
        """List refunds with optional filters."""

        refunds = list(
            self._refunds.values()
        )

        if transaction_id is not None:
            refunds = [
                refund
                for refund in refunds
                if refund.transaction_id
                == transaction_id
            ]

        if status is not None:
            refunds = [
                refund
                for refund in refunds
                if refund.status == status
            ]

        return refunds

    def complete_refund(
        self,
        refund_id: str,
    ) -> Refund:
        """Complete a refund."""

        refund = self._require_refund(
            refund_id
        )

        refund.status = RefundStatus.COMPLETED
        refund.updated_at = _utc_now()

        return refund

    def reject_refund(
        self,
        refund_id: str,
        reason: str = "",
    ) -> Refund:
        """Reject a refund."""

        refund = self._require_refund(
            refund_id
        )

        refund.status = RefundStatus.REJECTED
        refund.reason = reason
        refund.updated_at = _utc_now()

        return refund

    # =========================================================
    # STATUS
    # =========================================================

    def status(self) -> dict:
        """Return safe monetization runtime status."""

        return {
            "service": "MUKTI_MAHAL_MONETIZATION",
            "plans": len(self._plans),
            "subscriptions": len(
                self._subscriptions
            ),
            "transactions": len(
                self._transactions
            ),
            "refunds": len(self._refunds),
        }

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    def _require_plan(
        self,
        plan_id: str,
    ) -> MonetizationPlan:
        """Return a plan or raise an error."""

        plan = self.get_plan(plan_id)

        if plan is None:
            raise ValueError(
                "Monetization plan not found."
            )

        return plan

    def _require_subscription(
        self,
        subscription_id: str,
    ) -> Subscription:
        """Return a subscription or raise an error."""

        subscription = self.get_subscription(
            subscription_id
        )

        if subscription is None:
            raise ValueError(
                "Subscription not found."
            )

        return subscription

    def _require_transaction(
        self,
        transaction_id: str,
    ) -> Transaction:
        """Return a transaction or raise an error."""

        transaction = self.get_transaction(
            transaction_id
        )

        if transaction is None:
            raise ValueError(
                "Transaction not found."
            )

        return transaction

    def _require_refund(
        self,
        refund_id: str,
    ) -> Refund:
        """Return a refund or raise an error."""

        refund = self.get_refund(refund_id)

        if refund is None:
            raise ValueError(
                "Refund not found."
            )

        return refund


__all__ = [
    "PlanStatus",
    "SubscriptionStatus",
    "TransactionStatus",
    "RefundStatus",
    "PaymentType",
    "MonetizationPlan",
    "Subscription",
    "Transaction",
    "Refund",
    "MuktiMahalMonetization",
]
