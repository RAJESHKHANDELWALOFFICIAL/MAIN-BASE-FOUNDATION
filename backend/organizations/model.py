from dataclasses import dataclass


@dataclass
class Organization:

    organization_id: str
    organization_name: str
    display_name: str
    owner_id: str
    email: str
    phone: str
    website: str
    organization_type: str = "BUSINESS"
    status: str = "ACTIVE"
