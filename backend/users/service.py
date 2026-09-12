from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Optional

from backend.database.service import DatabaseService
from backend.users.model import User


class UserService:
    """MAIN BASE FOUNDATION User Service."""

    PASSWORD_ITERATIONS = 310000
    PASSWORD_SALT_BYTES = 16

    def __init__(self):
        self.database = DatabaseService()
        self.initialize()

    # ------------------------------------------------------------------
    # INITIALIZATION
    # ------------------------------------------------------------------

    def initialize(self):
        """Initialize the users table."""

        self.database.initialize()

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                phone TEXT,
                password TEXT,
                password_hash TEXT,
                role TEXT DEFAULT 'USER',
                status TEXT DEFAULT 'ACTIVE'
            )
            """
        )

        return {
            "service": "UserService",
            "status": "INITIALIZED",
        }

    # ------------------------------------------------------------------
    # PASSWORD SECURITY
    # ------------------------------------------------------------------

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Create a secure PBKDF2-HMAC-SHA256 password hash."""

        if not password:
            raise ValueError("Password cannot be empty.")

        salt = secrets.token_bytes(cls.PASSWORD_SALT_BYTES)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            cls.PASSWORD_ITERATIONS,
        )

        return (
            f"pbkdf2_sha256$"
            f"{cls.PASSWORD_ITERATIONS}$"
            f"{salt.hex()}$"
            f"{password_hash.hex()}"
        )

    @classmethod
    def verify_password(
        cls,
        password: str,
        stored_hash: str,
    ) -> bool:
        """Verify a password against a stored PBKDF2 hash."""

        if not password or not stored_hash:
            return False

        try:
            algorithm, iterations, salt_hex, hash_hex = (
                stored_hash.split("$")
            )

            if algorithm != "pbkdf2_sha256":
                return False

            expected_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                bytes.fromhex(salt_hex),
                int(iterations),
            )

            return hmac.compare_digest(
                expected_hash.hex(),
                hash_hex,
            )

        except (ValueError, TypeError):
            return False

    # ------------------------------------------------------------------
    # USER CREATION
    # ------------------------------------------------------------------

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
        """Create a User model and securely hash the password."""

        password_hash = self.hash_password(password)

        user = User(
            user_id=user_id,
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            role=role,
            status=status,
        )

        user._password_hash = password_hash

        return user

    # ------------------------------------------------------------------
    # SAVE
    # ------------------------------------------------------------------

    def save_user(self, user: User):
        """Save a user with a secure password hash."""

        password_hash = getattr(
            user,
            "_password_hash",
            None,
        )

        if not password_hash:
            raise ValueError(
                "Password hash is required to save a user."
            )

        self.database.execute(
            """
            INSERT OR REPLACE INTO users (
                user_id,
                full_name,
                username,
                email,
                phone,
                password,
                password_hash,
                role,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user.user_id,
                user.full_name,
                user.username,
                user.email,
                user.phone,
                "",
                password_hash,
                user.role,
                user.status,
            ),
        )

        return user

    # ------------------------------------------------------------------
    # USER RETRIEVAL
    # ------------------------------------------------------------------

    def _row_to_user(self, row) -> User:
        """Convert a database row into a safe User object."""

        return User(
            user_id=row["user_id"],
            full_name=row["full_name"],
            username=row["username"],
            email=row["email"],
            phone=row["phone"],
            role=row["role"],
            status=row["status"],
        )

    def get_user(
        self,
        user_id: str,
    ) -> Optional[User]:
        """Return one user without password credentials."""

        row = self.database.fetchone(
            """
            SELECT
                user_id,
                full_name,
                username,
                email,
                phone,
                role,
                status
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )

        if row is None:
            return None

        return self._row_to_user(row)

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

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
        """Update an existing user securely."""

        password_hash = self.hash_password(password)

        self.database.execute(
            """
            UPDATE users
            SET
                full_name = ?,
                username = ?,
                email = ?,
                phone = ?,
                password = ?,
                password_hash = ?,
                role = ?,
                status = ?
            WHERE user_id = ?
            """,
            (
                full_name,
                username,
                email,
                phone,
                "",
                password_hash,
                role,
                status,
                user_id,
            ),
        )

        return self.get_user(user_id)

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # LIST
    # ------------------------------------------------------------------

    def get_all_users(self):
        """Return all users without password credentials."""

        rows = self.database.fetchall(
            """
            SELECT
                user_id,
                full_name,
                username,
                email,
                phone,
                role,
                status
            FROM users
            ORDER BY rowid
            """
        )

        return [
            self._row_to_user(row)
            for row in rows
        ]

    # ------------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------------

    def search_user_by_username(
        self,
        username: str,
    ):
        """Search for a user without returning password credentials."""

        row = self.database.fetchone(
            """
            SELECT
                user_id,
                full_name,
                username,
                email,
                phone,
                role,
                status
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        if row is None:
            return None

        return self._row_to_user(row)

    # ------------------------------------------------------------------
    # PASSWORD VERIFICATION
    # ------------------------------------------------------------------

    def verify_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """Verify a user's password without exposing the password."""

        row = self.database.fetchone(
            """
            SELECT password_hash
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        if row is None:
            return False

        return self.verify_password(
            password,
            row["password_hash"],
        )
