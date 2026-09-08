"""
MAIN BASE FOUNDATION
Central Persistent Identity and Naming Engine

Maintains the complete identity mapping of entities
inside MAIN-BASE-FOUNDATION.

Supported representations:

    small
    capital
    bold
    icon_emoji
"""

from dataclasses import dataclass
from typing import Optional

from backend.engines.database.manager import DatabaseEngine


@dataclass
class Identity:
    """
    Represents all identity forms of one entity.
    """

    entity_id: str
    small: str
    capital: str
    bold: str
    icon_emoji: str

    def to_dict(self) -> dict:
        """Return the complete identity mapping."""

        return {
            "entity_id": self.entity_id,
            "small": self.small,
            "capital": self.capital,
            "bold": self.bold,
            "icon_emoji": self.icon_emoji,
        }

    def get(self, identity_type: str) -> str:
        """Return one identity representation."""

        identities = {
            "small": self.small,
            "capital": self.capital,
            "bold": self.bold,
            "icon_emoji": self.icon_emoji,
        }

        if identity_type not in identities:
            raise ValueError(
                f"Unknown identity type: {identity_type}"
            )

        return identities[identity_type]


class IdentityManager:
    """
    Persistent central identity manager.

    Identity records are stored in the central database so
    identity mappings survive process restarts.
    """

    TABLE_NAME = "foundation_identity"

    ALLOWED_TYPES = {
        "small",
        "capital",
        "bold",
        "icon_emoji",
    }

    def __init__(
        self,
        database: Optional[DatabaseEngine] = None,
    ):
        self.database = database or DatabaseEngine()
        self._initialize()

    # ==========================================================
    # DATABASE INITIALIZATION
    # ==========================================================

    def _initialize(self) -> None:
        """Create the identity table when required."""

        self.database.create_table(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                entity_id TEXT PRIMARY KEY,
                small TEXT NOT NULL,
                capital TEXT NOT NULL,
                bold TEXT NOT NULL,
                icon_emoji TEXT NOT NULL
            )
            """
        )

        self.database.execute(
            f"""
            CREATE INDEX IF NOT EXISTS
            idx_{self.TABLE_NAME}_small
            ON {self.TABLE_NAME}(small)
            """
        )

        self.database.execute(
            f"""
            CREATE INDEX IF NOT EXISTS
            idx_{self.TABLE_NAME}_capital
            ON {self.TABLE_NAME}(capital)
            """
        )

    # ==========================================================
    # VALIDATION
    # ==========================================================

    def _validate_identity(
        self,
        identity: Identity,
    ) -> None:
        """Validate an identity before persistence."""

        if not identity.entity_id:
            raise ValueError(
                "entity_id is required."
            )

        if not identity.small:
            raise ValueError(
                "small identity is required."
            )

        if not identity.capital:
            raise ValueError(
                "capital identity is required."
            )

        if not identity.bold:
            raise ValueError(
                "bold identity is required."
            )

        if not identity.icon_emoji:
            raise ValueError(
                "icon_emoji identity is required."
            )

    # ==========================================================
    # REGISTER
    # ==========================================================

    def register(
        self,
        identity: Identity,
    ) -> Identity:
        """Persist a new identity mapping."""

        self._validate_identity(identity)

        existing = self.get(
            identity.entity_id
        )

        if existing is not None:
            raise ValueError(
                "Identity already registered: "
                f"{identity.entity_id}"
            )

        self.database.execute(
            f"""
            INSERT INTO {self.TABLE_NAME} (
                entity_id,
                small,
                capital,
                bold,
                icon_emoji
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                identity.entity_id,
                identity.small,
                identity.capital,
                identity.bold,
                identity.icon_emoji,
            ),
        )

        return identity

    # ==========================================================
    # GET
    # ==========================================================

    def get(
        self,
        entity_id: str,
    ) -> Optional[Identity]:
        """Return one identity mapping."""

        row = self.database.fetch_one(
            f"""
            SELECT
                entity_id,
                small,
                capital,
                bold,
                icon_emoji
            FROM {self.TABLE_NAME}
            WHERE entity_id = ?
            """,
            (entity_id,),
        )

        if row is None:
            return None

        return Identity(
            entity_id=row["entity_id"],
            small=row["small"],
            capital=row["capital"],
            bold=row["bold"],
            icon_emoji=row["icon_emoji"],
        )

    def require(
        self,
        entity_id: str,
    ) -> Identity:
        """Return an identity or raise KeyError."""

        identity = self.get(entity_id)

        if identity is None:
            raise KeyError(
                f"Identity not found: {entity_id}"
            )

        return identity

    # ==========================================================
    # GET REPRESENTATION
    # ==========================================================

    def get_representation(
        self,
        entity_id: str,
        identity_type: str,
    ) -> str:
        """Return one specific identity representation."""

        if identity_type not in self.ALLOWED_TYPES:
            raise ValueError(
                f"Unknown identity type: "
                f"{identity_type}"
            )

        identity = self.require(
            entity_id
        )

        return identity.get(
            identity_type
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        entity_id: str,
        **changes,
    ) -> Identity:
        """Update one or more identity representations."""

        identity = self.require(
            entity_id
        )

        unknown_fields = (
            set(changes.keys())
            - self.ALLOWED_TYPES
        )

        if unknown_fields:
            raise ValueError(
                "Unknown identity fields: "
                f"{sorted(unknown_fields)}"
            )

        if not changes:
            return identity

        assignments = []
        parameters = []

        for field in (
            "small",
            "capital",
            "bold",
            "icon_emoji",
        ):
            if field in changes:

                value = changes[field]

                if not value:
                    raise ValueError(
                        f"{field} cannot be empty."
                    )

                assignments.append(
                    f"{field} = ?"
                )

                parameters.append(
                    value
                )

                setattr(
                    identity,
                    field,
                    value,
                )

        parameters.append(
            entity_id
        )

        self.database.execute(
            f"""
            UPDATE {self.TABLE_NAME}
            SET {", ".join(assignments)}
            WHERE entity_id = ?
            """,
            tuple(parameters),
        )

        return identity

    # ==========================================================
    # REMOVE
    # ==========================================================

    def remove(
        self,
        entity_id: str,
    ) -> bool:
        """Remove an identity mapping."""

        self.require(
            entity_id
        )

        self.database.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            WHERE entity_id = ?
            """,
            (entity_id,),
        )

        return True

    # ==========================================================
    # SEARCH
    # ==========================================================

    def find_by_small(
        self,
        small: str,
    ) -> Optional[Identity]:
        """Find an identity using its small representation."""

        row = self.database.fetch_one(
            f"""
            SELECT
                entity_id,
                small,
                capital,
                bold,
                icon_emoji
            FROM {self.TABLE_NAME}
            WHERE small = ?
            """,
            (small,),
        )

        if row is None:
            return None

        return Identity(
            entity_id=row["entity_id"],
            small=row["small"],
            capital=row["capital"],
            bold=row["bold"],
            icon_emoji=row["icon_emoji"],
        )

    def find_by_capital(
        self,
        capital: str,
    ) -> Optional[Identity]:
        """Find an identity using its capital representation."""

        row = self.database.fetch_one(
            f"""
            SELECT
                entity_id,
                small,
                capital,
                bold,
                icon_emoji
            FROM {self.TABLE_NAME}
            WHERE capital = ?
            """,
            (capital,),
        )

        if row is None:
            return None

        return Identity(
            entity_id=row["entity_id"],
            small=row["small"],
            capital=row["capital"],
            bold=row["bold"],
            icon_emoji=row["icon_emoji"],
        )

    # ==========================================================
    # LIST
    # ==========================================================

    def list_all(self) -> list[dict]:
        """Return all persistent identity mappings."""

        rows = self.database.fetch_all(
            f"""
            SELECT
                entity_id,
                small,
                capital,
                bold,
                icon_emoji
            FROM {self.TABLE_NAME}
            ORDER BY entity_id COLLATE NOCASE
            """
        )

        return [
            {
                "entity_id": row["entity_id"],
                "small": row["small"],
                "capital": row["capital"],
                "bold": row["bold"],
                "icon_emoji": row["icon_emoji"],
            }
            for row in rows
        ]

    # ==========================================================
    # COUNT
    # ==========================================================

    def count(self) -> int:
        """Return total identity mappings."""

        row = self.database.fetch_one(
            f"""
            SELECT COUNT(*) AS total
            FROM {self.TABLE_NAME}
            """
        )

        return int(
            row["total"]
        )

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear(self) -> None:
        """Clear all identity mappings."""

        self.database.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            """
        )


identity_manager = IdentityManager()


__all__ = [
    "Identity",
    "IdentityManager",
    "identity_manager",
]
