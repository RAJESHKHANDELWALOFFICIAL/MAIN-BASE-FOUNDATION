from backend.database.service import DatabaseService
from backend.organizations.model import Organization


class OrganizationService:

    def __init__(self):
        self.database = DatabaseService()

    def initialize(self):

        self.database.initialize()

        self.database.execute("""
        CREATE TABLE IF NOT EXISTS organizations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            organization_id TEXT UNIQUE,
            organization_name TEXT,
            display_name TEXT,
            owner_id TEXT,

            email TEXT,
            phone TEXT,
            website TEXT,

            organization_type TEXT,
            status TEXT

        )
        """)

        return {
            "organizations": "Initialized",
            "status": "READY"
        }

    def create_organization(
        self,
        organization_id,
        organization_name,
        display_name,
        owner_id,
        email,
        phone,
        website,
        organization_type="BUSINESS",
        status="ACTIVE",
    ):

        return Organization(
            organization_id=organization_id,
            organization_name=organization_name,
            display_name=display_name,
            owner_id=owner_id,
            email=email,
            phone=phone,
            website=website,
            organization_type=organization_type,
            status=status,
        )
