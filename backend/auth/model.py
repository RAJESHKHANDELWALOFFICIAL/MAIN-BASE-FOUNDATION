from dataclasses import dataclass


@dataclass
class AuthenticationInfo:
    authenticated: bool
    master_id: str
    full_name: str
    username: str
    status: str
