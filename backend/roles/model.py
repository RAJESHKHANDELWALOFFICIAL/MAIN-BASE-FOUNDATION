from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Role:

    id: Optional[int] = None

    role_id: str = ""

    role_name: str = ""

    description: str = ""

    level: int = 1

    status: str = "ACTIVE"

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
