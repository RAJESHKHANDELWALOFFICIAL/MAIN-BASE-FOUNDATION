from backend.identity.model import MasterIdentity
from backend.database.service import DatabaseService


class IdentityService:

    def __init__(self):
        self.database = DatabaseService()

    def create_identity(
        self,
        master_id,
        full_name,
        display_name,
        username,
        email,
        phone,
    ):
        return MasterIdentity(
            master_id=master_id,
            full_name=full_name,
            display_name=display_name,
            primary_username=username,
            email=email,
            phone=phone,
        )

    def save_identity(self, identity):
        self.database.execute(
            """
            INSERT OR REPLACE INTO master_identity
            (
                master_id,
                full_name,
                display_name,
                username,
                email,
                phone,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                identity.master_id,
                identity.full_name,
                identity.display_name,
                identity.primary_username,
                identity.email,
                identity.phone,
                identity.status,
            ),
        )

    def get_identity(self, master_id):
        row = self.database.fetchone(
            """
            SELECT
                master_id,
                full_name,
                display_name,
                username,
                email,
                phone,
                status
            FROM master_identity
            WHERE master_id = ?
            """,
            (master_id,),
        )

        if row is None:
            return None

        return MasterIdentity(
            master_id=row[0],
            full_name=row[1],
            display_name=row[2],
            primary_username=row[3],
            email=row[4],
            phone=row[5],
            status=row[6],
        )

    def update_identity(
        self,
        master_id,
        full_name,
        display_name,
        username,
        email,
        phone,
        status,
    ):
        self.database.execute(
            """
            UPDATE master_identity
            SET
                full_name = ?,
                display_name = ?,
                username = ?,
                email = ?,
                phone = ?,
                status = ?
            WHERE master_id = ?
            """,
            (
                full_name,
                display_name,
                username,
                email,
                phone,
                status,
                master_id,
            ),
        )

    def delete_identity(self, master_id):
        self.database.execute(
            """
            DELETE FROM master_identity
            WHERE master_id = ?
            """,
            (master_id,),
        )

    def initialize(self):
        self.database.initialize()

        identity = self.create_identity(
            master_id="MBF-000001",
            full_name="DR RAJESH KHANDELWAL IBC",
            display_name="DR RAJESH KHANDELWAL IBC",
            username="RAJESHKHANDELWALOFFICIAL",
            email="demo@example.com",
            phone="+910000000000",
        )

        self.save_identity(identity)

        return identity
