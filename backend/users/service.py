from backend.users.model import User
from backend.database.service import DatabaseService


class UserService:

    def __init__(self):
        self.database = DatabaseService()

    def initialize(self):
        self.database.initialize()

        self.database.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE,
            full_name TEXT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            phone TEXT,
            password TEXT,
            role TEXT,
            status TEXT
        )
        """)

        return {
            "users": "Initialized",
            "status": "READY"
        }

    def create_user(
        self,
        user_id,
        full_name,
        username,
        email,
        phone,
        password,
        role="USER",
        status="ACTIVE"
    ):
        return User(
            user_id=user_id,
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            password=password,
            role=role,
            status=status,
        )

    def save_user(self, user):

        self.database.execute(
            """
            INSERT OR REPLACE INTO users
            (
                user_id,
                full_name,
                username,
                email,
                phone,
                password,
                role,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user.user_id,
                user.full_name,
                user.username,
                user.email,
                user.phone,
                user.password,
                user.role,
                user.status,
            ),
        )

    def get_user(self, user_id):

        row = self.database.fetchone(
            """
            SELECT
                user_id,
                full_name,
                username,
                email,
                phone,
                password,
                role,
                status
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )

        if row is None:
            return None

        return User(
            user_id=row[0],
            full_name=row[1],
            username=row[2],
            email=row[3],
            phone=row[4],
            password=row[5],
            role=row[6],
            status=row[7],
        )

    def delete_user(self, user_id):

        self.database.execute(
            "DELETE FROM users WHERE user_id = ?",
            (user_id,),
        )
