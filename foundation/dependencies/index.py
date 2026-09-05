"""
MAIN BASE FOUNDATION
Dependency and Reference Index

Maintains controlled relationships between
entities inside MAIN-BASE-FOUNDATION.
"""


class Dependency:
    """
    Represents one directed relationship between
    two foundation entities.
    """

    def __init__(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
    ):
        if not source_id:
            raise ValueError(
                "source_id is required."
            )

        if not target_id:
            raise ValueError(
                "target_id is required."
            )

        if not relationship:
            raise ValueError(
                "relationship is required."
            )

        self.source_id = source_id
        self.target_id = target_id
        self.relationship = relationship

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship": self.relationship,
        }


class DependencyIndex:
    """
    Central dependency and reference manager.
    """

    def __init__(self):
        self._dependencies: list[Dependency] = []

    def add(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
    ) -> Dependency:

        if self.exists(
            source_id,
            target_id,
            relationship,
        ):
            raise ValueError(
                "Dependency already exists."
            )

        dependency = Dependency(
            source_id=source_id,
            target_id=target_id,
            relationship=relationship,
        )

        self._dependencies.append(
            dependency
        )

        return dependency

    def exists(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
    ) -> bool:

        return any(
            dependency.source_id == source_id
            and dependency.target_id == target_id
            and dependency.relationship == relationship
            for dependency in self._dependencies
        )

    def remove(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
    ) -> bool:

        for dependency in self._dependencies:

            if (
                dependency.source_id == source_id
                and dependency.target_id == target_id
                and dependency.relationship == relationship
            ):
                self._dependencies.remove(
                    dependency
                )
                return True

        raise KeyError(
            "Dependency not found."
        )

    def get_dependencies(
        self,
        source_id: str,
    ) -> list[dict]:

        return [
            dependency.to_dict()
            for dependency in self._dependencies
            if dependency.source_id == source_id
        ]

    def get_dependents(
        self,
        target_id: str,
    ) -> list[dict]:

        return [
            dependency.to_dict()
            for dependency in self._dependencies
            if dependency.target_id == target_id
        ]

    def list_all(self) -> list[dict]:

        return [
            dependency.to_dict()
            for dependency in self._dependencies
        ]


dependency_index = DependencyIndex()


__all__ = [
    "Dependency",
    "DependencyIndex",
    "dependency_index",
]
