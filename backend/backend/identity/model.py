from dataclasses import dataclass


@dataclass
class MasterIdentity:
    master_id: str
    full_name: str
    display_name: str
    primary_username: str
    email: str
    phone: str
    status: str = "active"
