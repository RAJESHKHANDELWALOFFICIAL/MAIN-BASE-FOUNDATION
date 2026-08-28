"""Supreme Ecosystem API."""

from backend.engines.ecosystem import EcosystemManager


class EcosystemAPI:
    """API facade for the Supreme Ecosystem."""

    def __init__(self):
        self.engine = EcosystemManager()

    def status(self) -> dict:
        """Return Supreme Ecosystem status."""

        return self.engine.status()

    def health(self) -> dict:
        """Return Supreme Ecosystem health."""

        return self.engine.health()

    def list(self) -> list:
        """Return all registered ecosystems."""

        return self.engine.list()

    def names(self) -> list:
        """Return all registered ecosystem names."""

        return self.engine.names()

    def get(
        self,
        ecosystem_id: str,
    ) -> dict:
        """Return one registered ecosystem."""

        return self.engine.get(
            ecosystem_id
        )

    def exists(
        self,
        ecosystem_id: str,
    ) -> bool:
        """Check whether an ecosystem exists."""

        return self.engine.exists(
            ecosystem_id
        )
