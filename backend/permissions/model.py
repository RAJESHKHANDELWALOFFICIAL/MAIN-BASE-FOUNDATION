from dataclasses import dataclass


@dataclass
class Permission:

    permission_id: str
    permission_name: str
    display_name: str
    description: str

    status: str = "ACTIVE"
