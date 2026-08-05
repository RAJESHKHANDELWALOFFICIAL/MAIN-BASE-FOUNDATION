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

    def save_organization(self, organization):

        self.database.execute(
            """
            INSERT OR REPLACE INTO organizations
            (
                organization_id,
                organization_name,
                display_name,
                owner_id,
                email,
                phone,
                website,
                organization_type,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                organization.organization_id,
                organization.organization_name,
                organization.display_name,
                organization.owner_id,
                organization.email,
                organization.phone,
                organization.website,
                organization.organization_type,
                organization.status,
            ),
        )

    def get_organization(self, organization_id):

        row = self.database.fetchone(
            """
            SELECT
                organization_id,
                organization_name,
                display_name,
                owner_id,
                email,
                phone,
                website,
                organization_type,
                status
            FROM organizations
            WHERE organization_id = ?
            """,
            (organization_id,),
        )

        if row is None:
            return None

        return Organization(
            organization_id=row[0],
            organization_name=row[1],
            display_name=row[2],
            owner_id=row[3],
            email=row[4],
            phone=row[5],
            website=row[6],
            organization_type=row[7],
            status=row[8],
        )

    def update_organization(
        self,
        organization_id,
        organization_name,
        display_name,
        owner_id,
        email,
        phone,
        website,
        organization_type,
        status,
    ):

        self.database.execute(
            """
            UPDATE organizations
            SET
                organization_name = ?,
                display_name = ?,
                owner_id = ?,
                email = ?,
                phone = ?,
                website = ?,
                organization_type = ?,
                status = ?
            WHERE organization_id = ?
            """,
            (
                organization_name,
                display_name,
                owner_id,
                email,
                phone,
                website,
                organization_type,
                status,
                organization_id,
            ),
        )

    def delete_organization(self, organization_id):

        self.database.execute(
            """
            DELETE FROM organizations
            WHERE organization_id = ?
            """,
            (organization_id,),
        )

    def get_all_organizations(self):

        return self.database.fetchall(
            """
            SELECT
                organization_id,
                organization_name,
                display_name,
                owner_id,
                email,
                phone,
                website,
                organization_type,
                status
            FROM organizations
            """
        )

    def search_organization_by_name(self, organization_name):

        return self.database.fetchone(
            """
            SELECT
                organization_id,
                organization_name,
                display_name,
                owner_id,
                email,
                phone,
                website,
                organization_type,
                status
            FROM organizations
            WHERE organization_name = ?
            """,
            (organization_name,),
        )
