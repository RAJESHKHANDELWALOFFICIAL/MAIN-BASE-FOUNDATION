"""
MAIN BASE FOUNDATION
Central Foundation Registry

Maintains the canonical registry of entities
belonging to MAIN-BASE-FOUNDATION.
"""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class RegistryEntry:
    """
    Canonical record for one foundation entity.
    """

    entity_id: str
    entity_type: str
    path: str
    identity_id: str
    status: str = "active"

    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        now = datetime.now(timezone.utc).isoformat()

        if not self.created_at:
            self.created_at = now

        if not self.updated_at:
            self.updated_at = now

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "path": self.path,
            "identity_id": self.identity_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class FoundationRegistry:
    """
    Central registry for all foundation entities.
    """

    def __init__(self):
        self._entries: dict[str, RegistryEntry] = {}

    def register(
        self,
        entry: RegistryEntry
    ) -> RegistryEntry:

        if entry.entity_id in self._entries:
            raise ValueError(
                f"Entity already registered: "
                f"{entry.entity_id}"
            )

        self._entries[
            entry.entity_id
        ] = entry

        return entry

    def get(
        self,
        entity_id: str
    ) -> RegistryEntry:

        if entity_id not in self._entries:
            raise KeyError(
                f"Entity not found: {entity_id}"
            )

        return self._entries[entity_id]

    def update_path(
        self,
        entity_id: str,
        path: str
    ) -> RegistryEntry:

        entry = self.get(entity_id)

        entry.path = path
        entry.updated_at = (
            datetime.now(timezone.utc).isoformat()
        )

        return entry

    def remove(
        self,
        entity_id: str
    ) -> bool:

        if entity_id not in self._entries:
            raise KeyError(
                f"Entity not found: {entity_id}"
            )

        del self._entries[entity_id]

        return True

    def list_all(self) -> list[dict]:

        return [
            entry.to_dict()
            for entry in self._entries.values()
        ]


registry = FoundationRegistry()


__all__ = [
    "RegistryEntry",
    "FoundationRegistry",
    "registry",
]
