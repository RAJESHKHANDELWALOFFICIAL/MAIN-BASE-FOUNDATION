from backend.supreme.model import SupremeOwner
from backend.database.service import DatabaseService


class SupremeService:

    def __init__(self):
        self.database = DatabaseService()

    def initialize(self):

        self.database.initialize()

        self.database.execute("""
        CREATE TABLE IF NOT EXISTS supreme_owner (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            master_id TEXT UNIQUE,

            supreme_id TEXT UNIQUE,

            owner_name TEXT,

            username TEXT UNIQUE,

            email TEXT,

            phone TEXT,

            password TEXT,

            role TEXT,

            level INTEGER,

            status TEXT,

            two_factor_enabled INTEGER,

            recovery_email TEXT,

            recovery_phone TEXT,

            dashboard_name TEXT,

            dashboard_theme TEXT,

            system_version TEXT,

            created_at TEXT,

            updated_at TEXT
        )
        """)

        return {
            "supreme": "Initialized",
            "status": "READY"
        }

    def create_owner(
        self,
        master_id,
        supreme_id,
        owner_name,
        username,
        email,
        phone,
        password,
        role="SUPREME_OWNER",
        level=100,
        status="ACTIVE",
        two_factor_enabled=False,
        recovery_email=None,
        recovery_phone=None,
        dashboard_name="🔱 🕉️ SUPREME SHIV SHAKTI SYSTEM 🕉️ 🔱",
        dashboard_theme="SUPREME",
        system_version="1.0.0"
    ):

        return SupremeOwner(
            master_id=master_id,
            supreme_id=supreme_id,
            owner_name=owner_name,
            username=username,
            email=email,
            phone=phone,
            password=password,
            role=role,
            level=level,
            status=status,
            two_factor_enabled=two_factor_enabled,
            recovery_email=recovery_email,
            recovery_phone=recovery_phone,
            dashboard_name=dashboard_name,
            dashboard_theme=dashboard_theme,
            system_version=system_version
        )

    def save_owner(self, owner):

        self.database.execute(
            """
            INSERT OR REPLACE INTO supreme_owner (
                master_id,
                supreme_id,
                owner_name,
                username,
                email,
                phone,
                password,
                role,
                level,
                status,
                two_factor_enabled,
                recovery_email,
                recovery_phone,
                dashboard_name,
                dashboard_theme,
                system_version,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                owner.master_id,
                owner.supreme_id,
                owner.owner_name,
                owner.username,
                owner.email,
                owner.phone,
                owner.password,
                owner.role,
                owner.level,
                owner.status,
                int(owner.two_factor_enabled),
                owner.recovery_email,
                owner.recovery_phone,
                owner.dashboard_name,
                owner.dashboard_theme,
                owner.system_version,
                owner.created_at,
                owner.updated_at
            )
        )

    def get_owner(self):

        return self.database.fetchone(
            "SELECT * FROM supreme_owner LIMIT 1"
        )

    def list_owner(self):

        return self.database.fetchall(
            "SELECT * FROM supreme_owner"
        )

    def owner_exists(self):

        row = self.database.fetchone(
            "SELECT id FROM supreme_owner LIMIT 1"
        )

        return row is not None

    def update_owner(self, owner):

        self.database.execute(
            """
            UPDATE supreme_owner
            SET
                owner_name=?,
                username=?,
                email=?,
                phone=?,
                password=?,
                role=?,
                level=?,
                status=?,
                two_factor_enabled=?,
                recovery_email=?,
                recovery_phone=?,
                dashboard_name=?,
                dashboard_theme=?,
                system_version=?,
                updated_at=?
            WHERE supreme_id=?
            """,
            (
                owner.owner_name,
                owner.username,
                owner.email,
                owner.phone,
                owner.password,
                owner.role,
                owner.level,
                owner.status,
                int(owner.two_factor_enabled),
                owner.recovery_email,
                owner.recovery_phone,
                owner.dashboard_name,
                owner.dashboard_theme,
                owner.system_version,
                owner.updated_at,
                owner.supreme_id
            )
        )

    def delete_owner(self, supreme_id):

        self.database.execute(
            """
            DELETE FROM supreme_owner
            WHERE supreme_id=?
            """,
            (supreme_id,)
        )

    def login(self, identifier):

        return self.database.fetchone(
            """
            SELECT *
            FROM supreme_owner
            WHERE username=?
               OR email=?
               OR phone=?
            """,
            (
                identifier,
                identifier,
                identifier
            )
        )

    def logout(self):

        return {
            "status": "LOGOUT SUCCESS"
        }

    def change_password(
        self,
        supreme_id,
        password
    ):

        self.database.execute(
            """
            UPDATE supreme_owner
            SET password=?
            WHERE supreme_id=?
            """,
            (
                password,
                supreme_id
            )
        )

        return {
            "status": "PASSWORD UPDATED"
        }
