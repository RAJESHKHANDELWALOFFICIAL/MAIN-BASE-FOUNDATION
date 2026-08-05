from dataclasses import dataclass


@dataclass
class Team:

    team_id: str
    team_name: str
    display_name: str
    organization_id: str
    team_leader_id: str
    description: str

    status: str = "ACTIVE"
