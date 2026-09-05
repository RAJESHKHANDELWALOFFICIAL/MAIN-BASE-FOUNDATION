"""
MAIN BASE FOUNDATION
Central Identity and Naming Engine

Maintains the different identity representations
of entities inside MAIN-BASE-FOUNDATION.
"""


class Identity:
    """
    Represents one foundation entity and its
    supported naming/identity representations.
    """

    def __init__(
        self,
        entity_id: str,
        small: str,
        capital: str,
        bold: str,
        icon_emoji: str
    ):
        self.entity_id = entity_id
        self.small = small
        self.capital = capital
        self.bold = bold
        self.icon_emoji = icon_emoji

    def to_dict(self) -> dict:
        """
        Return the complete identity mapping.
        """

        return {
            "entity_id": self.entity_id,
            "small": self.small,
            "capital": self.capital,
            "bold": self.bold,
            "icon_emoji": self.icon_emoji
        }

    def get(self, identity_type: str) -> str:
        """
        Return one identity representation.
        """

        identities = {
            "small": self.small,
            "capital": self.capital,
            "bold": self.bold,
            "icon_emoji": self.icon_emoji
        }

        if identity_type not in identities:
            raise ValueError(
                f"Unknown identity type: {identity_type}"
            )

        return identities[identity_type]


class IdentityManager:
    """
    Central manager for entity identities.
    """

    def __init__(self):
        self._identities: dict[str, Identity] = {}

    def register(self, identity: Identity) -> Identity:

        if identity.entity_id in self._identities:
            raise ValueError(
                f"Identity already registered: "
                f"{identity.entity_id}"
            )

        self._identities[
            identity.entity_id
        ] = identity

        return identity

    def get(self, entity_id: str) -> Identity:

        if entity_id not in self._identities:
            raise KeyError(
                f"Identity not found: {entity_id}"
            )

        return self._identities[entity_id]

    def update(
        self,
        entity_id: str,
        **changes
    ) -> Identity:

        identity = self.get(entity_id)

        allowed_fields = {
            "small",
            "capital",
            "bold",
            "icon_emoji"
        }

        for field, value in changes.items():

            if field not in allowed_fields:
                raise ValueError(
                    f"Unknown identity field: {field}"
                )

            setattr(identity, field, value)

        return identity

    def remove(self, entity_id: str) -> bool:

        if entity_id not in self._identities:
            raise KeyError(
                f"Identity not found: {entity_id}"
            )

        del self._identities[entity_id]

        return True

    def list_all(self) -> list[dict]:

        return [
            identity.to_dict()
            for identity in self._identities.values()
        ]


identity_manager = IdentityManager()


__all__ = [
    "Identity",
    "IdentityManager",
    "identity_manager",
]
