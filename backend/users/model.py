from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    full_name: str
    username: str
    email: str
    phone: str
    password: str
    role: str = "USER"
    status: str = "ACTIVE"
