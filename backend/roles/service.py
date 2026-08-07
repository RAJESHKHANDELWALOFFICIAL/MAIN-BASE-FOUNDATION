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

            role_id TEXT UNIQUE NOT NULL,
            role_name TEXT UNIQUE NOT NULL,

            description TEXT,

            level INTEGER DEFAULT 1,

            status TEXT DEFAULT 'ACTIVE',

            created_at TEXT,
            updated_at TEXT

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
        level=1,
        status="ACTIVE"
    ):
        return Role(
            role_id=role_id,
            role_name=role_name,
            description=description,
            level=level,
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
                level,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                role.role_id,
                role.role_name,
                role.description,
                role.level,
                role.status,
                role.created_at,
                role.updated_at,
            ),
        )
def get_role(self, role_id):

    row = self.database.fetchone(
        """
        SELECT
            role_id,
            role_name,
            description,
            level,
            status,
            created_at,
            updated_at
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
        level=row[3],
        status=row[4],
        created_at=row[5],
        updated_at=row[6],
    )
    
def update_role(
    self,
    role_id,
    role_name,
    description,
    level,
    status,
):

    self.database.execute(
        """
        UPDATE roles
        SET
            role_name = ?,
            description = ?,
            level = ?,
            status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE role_id = ?
        """,
        (
            role_name,
            description,
            level,
            status,
            role_id,
        ),
    )
    
