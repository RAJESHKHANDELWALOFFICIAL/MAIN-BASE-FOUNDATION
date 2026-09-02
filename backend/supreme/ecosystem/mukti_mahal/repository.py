"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Repository Layer

Provides repository abstractions for Mukti Mahal domain data.

The repository layer keeps data-access concerns separate from
business/service logic so the underlying storage can later be
replaced with SQLite, PostgreSQL, or another database.

No credentials, passwords, OTPs, payment secrets, or authentication
secrets are stored here.
"""

from __future__ import annotations

from typing import Dict, Generic, List, Optional, TypeVar

from .model import (
    BusinessCapabilityEvaluation,
    MuktiMahal,
    MuktiMahalEstateArea,
    MuktiMahalFamilyMember,
    MuktiMahalFamilyVisit,
    MuktiMahalStaffMember,
    PratapGroup,
)


T = TypeVar("T")


class RepositoryError(Exception):
    """Base exception for repository-layer errors."""


class DuplicateEntityError(RepositoryError):
    """Raised when an entity with the same identifier already exists."""


class EntityNotFoundError(RepositoryError):
    """Raised when a requested entity does not exist."""


class InMemoryRepository(Generic[T]):
    """
    Generic in-memory repository.

    This is intentionally storage-agnostic. It provides the basic
    CRUD operations required by the Mukti Mahal service layer while
    keeping database implementation details out of the service.
    """

    def __init__(self) -> None:
        self._items: Dict[str, T] = {}

    def create(self, entity_id: str, entity: T) -> T:
        if not entity_id:
            raise ValueError("entity_id is required")

        if entity_id in self._items:
            raise DuplicateEntityError(
                f"Entity already exists: {entity_id}"
            )

        self._items[entity_id] = entity
        return entity

    def get(self, entity_id: str) -> Optional[T]:
        if not entity_id:
            return None

        return self._items.get(entity_id)

    def require(self, entity_id: str) -> T:
        entity = self.get(entity_id)

        if entity is None:
            raise EntityNotFoundError(
                f"Entity not found: {entity_id}"
            )

        return entity

    def update(self, entity_id: str, entity: T) -> T:
        if not entity_id:
            raise ValueError("entity_id is required")

        if entity_id not in self._items:
            raise EntityNotFoundError(
                f"Entity not found: {entity_id}"
            )

        self._items[entity_id] = entity
        return entity

    def upsert(self, entity_id: str, entity: T) -> T:
        if not entity_id:
            raise ValueError("entity_id is required")

        self._items[entity_id] = entity
        return entity

    def delete(self, entity_id: str) -> bool:
        if entity_id in self._items:
            del self._items[entity_id]
            return True

        return False

    def list_all(self) -> List[T]:
        return list(self._items.values())

    def count(self) -> int:
        return len(self._items)

    def clear(self) -> None:
        self._items.clear()


class MuktiMahalRepository:
    """
    Repository collection for the complete Mukti Mahal ecosystem.

    Each domain entity has its own repository. This keeps the service
    layer independent from the eventual database technology.
    """

    def __init__(self) -> None:
        self.mahals = InMemoryRepository[MuktiMahal]()
        self.groups = InMemoryRepository[PratapGroup]()
        self.family_members = InMemoryRepository[MuktiMahalFamilyMember]()
        self.staff_members = InMemoryRepository[MuktiMahalStaffMember]()
        self.estate_areas = InMemoryRepository[MuktiMahalEstateArea]()
        self.capability_evaluations = (
            InMemoryRepository[BusinessCapabilityEvaluation]()
        )
        self.family_visits = InMemoryRepository[MuktiMahalFamilyVisit]()

    def status(self) -> dict:
        """Return repository entity counts."""

        return {
            "mahals": self.mahals.count(),
            "groups": self.groups.count(),
            "family_members": self.family_members.count(),
            "staff_members": self.staff_members.count(),
            "estate_areas": self.estate_areas.count(),
            "capability_evaluations": self.capability_evaluations.count(),
            "family_visits": self.family_visits.count(),
        }

    def clear(self) -> None:
        """Clear all repository data."""

        self.mahals.clear()
        self.groups.clear()
        self.family_members.clear()
        self.staff_members.clear()
        self.estate_areas.clear()
        self.capability_evaluations.clear()
        self.family_visits.clear()


__all__ = [
    "RepositoryError",
    "DuplicateEntityError",
    "EntityNotFoundError",
    "InMemoryRepository",
    "MuktiMahalRepository",
]
