"""Supreme Ecosystem data models."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EcosystemIdentity:
    """Identity and capabilities of a registered ecosystem."""

    ecosystem_id: str
    name: str
    ecosystem_type: str

    repository_ref: Optional[str] = None

    status: str = "REGISTERED"

    enabled: bool = True

    capabilities: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    message: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert ecosystem identity to a JSON-friendly dictionary."""

        return {
            "ecosystem_id": self.ecosystem_id,
            "name": self.name,
            "ecosystem_type": self.ecosystem_type,
            "repository_ref": self.repository_ref,
            "status": self.status,
            "enabled": self.enabled,
            "capabilities": self.capabilities,
            "metadata": self.metadata,
            "message": self.message,
        }
