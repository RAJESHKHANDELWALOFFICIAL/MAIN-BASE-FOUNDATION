from backend.roles.model import Role
from backend.database.service import DatabaseService


class RoleService:

    def __init__(self):
        self.database = DatabaseService()

    def initialize(self):
        self.database.initialize()

        self.database.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id TEXT UNIQUE,
            role_name TEXT UNIQUE,
            description TEXT,
            status TEXT
        )
        """)

        return {
            "roles": "Initialized",
            "status": "READY"
        }

    def create_role(
        self,
        role_id,
        role_name,
        description,
        status="ACTIVE"
    ):
        return Role(
            role_id=role_id,
            role_name=role_name,
            description=description,
            status=status,
        )

    def save_role(self, role):

        self.database.execute(
            """
            INSERT OR REPLACE INTO roles
            (
                role_id,
                role_name,
                description,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                role.role_id,
                role.role_name,
                role.description,
                role.status,
            ),
        )

    def get_role(self, role_id):

        row = self.database.fetchone(
            """
            SELECT
                role_id,
                role_name,
                description,
                status
            FROM roles
            WHERE role_id = ?
            """,
            (role_id,),
        )

        if row is None:
            return None

        return Role(
            role_id=row[0],
            role_name=row[1],
            description=row[2],
            status=row[3],
        )

    def update_role(
        self,
        role_id,
        role_name,
        description,
        status,
    ):

        self.database.execute(
            """
            UPDATE roles
            SET
                role_name = ?,
                description = ?,
                status = ?
            WHERE role_id = ?
            """,
            (
                role_name,
                description,
                status,
                role_id,
            ),
        )

    def delete_role(self, role_id):

        self.database.execute(
            """
            DELETE FROM roles
            WHERE role_id = ?
            """,
            (role_id,),
        )

    def get_all_roles(self):

        return self.database.fetchall(
            """
            SELECT
                role_id,
                role_name,
                description,
                status
            FROM roles
            """
        )
