from typing import Optional

from backend.database.service import DatabaseService
from backend.users.model import User


class UserService:
    """MAIN BASE FOUNDATION User Service."""

    def __init__(self):
        self.database = DatabaseService()
        self.initialize()

    def initialize(self):
        """Initialize the users table."""

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                phone TEXT,
                password TEXT,
                role TEXT DEFAULT 'USER',
                status TEXT DEFAULT 'ACTIVE'
            )
            """
        )

        return {
            "service": "UserService",
            "status": "INITIALIZED",
        }

    def create_user(
        self,
        user_id: str,
        full_name: str,
        username: str,
        email: str,
        phone: str,
        password: str,
        role: str = "USER",
        status: str = "ACTIVE",
    ) -> User:
        """Create a User model."""

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

    def save_user(self, user: User):
        """Save a user into the database."""

        self.database.execute(
            """
            INSERT OR REPLACE INTO users (
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

        return user

    def get_user(
        self,
        user_id: str,
    ) -> Optional[User]:
        """Return one user by ID."""

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

    def update_user(
        self,
        user_id: str,
        full_name: str,
        username: str,
        email: str,
        phone: str,
        password: str,
        role: str,
        status: str,
    ):
        """Update an existing user."""

        self.database.execute(
            """
            UPDATE users
            SET
                full_name = ?,
                username = ?,
                email = ?,
                phone = ?,
                password = ?,
                role = ?,
                status = ?
            WHERE user_id = ?
            """,
            (
                full_name,
                username,
                email,
                phone,
                password,
                role,
                status,
                user_id,
            ),
        )

        return self.get_user(user_id)

    def delete_user(
        self,
        user_id: str,
    ):
        """Delete a user by ID."""

        self.database.execute(
            """
            DELETE FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )

        return {
            "user_id": user_id,
            "status": "DELETED",
        }

    def get_all_users(self):
        """Return all users."""

        rows = self.database.fetchall(
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
            ORDER BY rowid
            """
        )

        users = []

        for row in rows:
            users.append(
                User(
                    user_id=row[0],
                    full_name=row[1],
                    username=row[2],
                    email=row[3],
                    phone=row[4],
                    password=row[5],
                    role=row[6],
                    status=row[7],
                )
            )

        return users

    def search_user_by_username(
        self,
        username: str,
    ):
        """Search for a user by username."""

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
            WHERE username = ?
            """,
            (username,),
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
