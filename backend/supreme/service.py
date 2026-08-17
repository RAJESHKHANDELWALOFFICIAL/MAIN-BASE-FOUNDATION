"""
MAIN BASE FOUNDATION

SUPREME — Service Layer

Central SUPREME owner lifecycle, authentication foundation,
database persistence and system status service.

Security principles:
- Plaintext passwords are never stored.
- Passwords are stored as PBKDF2-HMAC-SHA256 hashes.
- Authentication is separated from authorization.
- SUPREME owner profile remains OWNER_ONLY.
- Database operations remain inside this service layer.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Any, Dict, Optional

from backend.database.service import DatabaseService
from backend.supreme.model import (
    SupremeOwner,
    SupremeRole,
    SupremeProfileVisibility,
)


# =========================================================
# 🔐 PASSWORD SECURITY
# =========================================================

_PASSWORD_ITERATIONS = 310_000
_SALT_BYTES = 32
_HASH_BYTES = 32


def _hash_password(password: str) -> str:
    """
    Create a secure PBKDF2-HMAC-SHA256 password hash.

    Stored format:

        pbkdf2_sha256$iterations$salt$hash
    """

    if not isinstance(password, str):
        raise TypeError(
            "Password must be a string."
        )

    if not password:
        raise ValueError(
            "Password cannot be empty."
        )

    salt = secrets.token_bytes(
        _SALT_BYTES
    )

    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        _PASSWORD_ITERATIONS,
        dklen=_HASH_BYTES,
    )

    return (
        "pbkdf2_sha256$"
        f"{_PASSWORD_ITERATIONS}$"
        f"{salt.hex()}$"
        f"{derived.hex()}"
    )


def _verify_password(
    password: str,
    stored_hash: str,
) -> bool:
    """
    Verify a password against a stored PBKDF2 hash.
    """

    if not isinstance(password, str):
        return False

    if not isinstance(stored_hash, str):
        return False

    try:
        algorithm, iterations, salt_hex, hash_hex = (
            stored_hash.split("$")
        )

        if algorithm != "pbkdf2_sha256":
            return False

        iterations_int = int(iterations)

        salt = bytes.fromhex(
            salt_hex
        )

        expected = bytes.fromhex(
            hash_hex
        )

        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations_int,
            dklen=len(expected),
        )

        return hmac.compare_digest(
            actual,
            expected,
        )

    except (
        ValueError,
        TypeError,
    ):
        return False


# =========================================================
# 👑 SUPREME SERVICE
# =========================================================

class SupremeService:
    """
    Central SUPREME service.

    Handles:

    - SUPREME owner
    - database initialization
    - owner persistence
    - owner lookup
    - authentication foundation
    - password changes
    - security metadata
    - service status
    """

    def __init__(
        self,
        database: Optional[
            DatabaseService
        ] = None,
    ) -> None:

        self.database = (
            database
            if database is not None
            else DatabaseService()
        )

        self._initialized = False

    # =====================================================
    # 🚀 INITIALIZE
    # =====================================================

    def initialize(self) -> Dict[str, str]:
        """
        Initialize SUPREME database structures.
        """

        self.database.initialize()

        # -------------------------------------------------
        # 👑 SUPREME OWNER
        # -------------------------------------------------

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS supreme_owner (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                master_id TEXT UNIQUE NOT NULL,

                supreme_id TEXT UNIQUE NOT NULL,

                owner_name TEXT NOT NULL,

                username TEXT UNIQUE NOT NULL,

                email TEXT,

                phone TEXT,

                role TEXT NOT NULL,

                level INTEGER NOT NULL DEFAULT 100,

                status TEXT NOT NULL DEFAULT 'ACTIVE',

                two_factor_enabled INTEGER
                    NOT NULL DEFAULT 0,

                recovery_email TEXT,

                recovery_phone TEXT,

                dashboard_name TEXT,

                dashboard_theme TEXT,

                profile_visibility TEXT
                    NOT NULL DEFAULT 'OWNER_ONLY',

                system_version TEXT,

                created_at TEXT,

                updated_at TEXT
            )
            """
        )

        # -------------------------------------------------
        # 🔐 SUPREME CREDENTIALS
        # -------------------------------------------------

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS supreme_credentials (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                supreme_id TEXT UNIQUE NOT NULL,

                password_hash TEXT NOT NULL,

                password_version TEXT
                    NOT NULL DEFAULT 'PBKDF2-SHA256',

                failed_attempts INTEGER
                    NOT NULL DEFAULT 0,

                locked INTEGER
                    NOT NULL DEFAULT 0,

                last_login_at TEXT,

                password_changed_at TEXT,

                created_at TEXT,

                updated_at TEXT,

                FOREIGN KEY (
                    supreme_id
                )
                REFERENCES supreme_owner (
                    supreme_id
                )
            )
            """
        )

        self._initialized = True

        return {
            "supreme": "Initialized",
            "status": "READY",
        }

    # =====================================================
    # 👑 CREATE OWNER
    # =====================================================

    def create_owner(
        self,
        master_id: str,
        supreme_id: str,
        owner_name: str,
        username: str,
        email: str,
        phone: str,
        password: str,
        role: str = "SUPREME_OWNER",
        level: int = 100,
        status: str = "ACTIVE",
        two_factor_enabled: bool = False,
        recovery_email: Optional[str] = None,
        recovery_phone: Optional[str] = None,
        dashboard_name: str = (
            "🔱 🕉️ SUPREME SHIV SHAKTI SYSTEM 🕉️ 🔱"
        ),
        dashboard_theme: str = "SUPREME",
        system_version: str = "1.0.0",
    ) -> SupremeOwner:
        """
        Create a SUPREME owner model.

        The plaintext password is immediately converted into
        a secure hash and is never placed into SupremeOwner.
        """

        if not password:
            raise ValueError(
                "SUPREME owner password cannot be empty."
            )

        if level < 0 or level > 100:
            raise ValueError(
                "SUPREME owner level must be "
                "between 0 and 100."
            )

        if role != SupremeRole.SUPREME_OWNER.value:
            raise ValueError(
                "SUPREME owner role must be "
                "SUPREME_OWNER."
            )

        owner = SupremeOwner(
            master_id=master_id,
            supreme_id=supreme_id,
            owner_name=owner_name,
            username=username,
            email=email,
            phone=phone,
            role=SupremeRole.SUPREME_OWNER,
            level=level,
            status=status,
            two_factor_enabled=two_factor_enabled,
            recovery_email=recovery_email,
            recovery_phone=recovery_phone,
            dashboard_name=dashboard_name,
            dashboard_theme=dashboard_theme,
            profile_visibility=(
                SupremeProfileVisibility.OWNER_ONLY
            ),
            system_version=system_version,
        )

        # -------------------------------------------------
        # 🔐 TEMPORARY INTERNAL HASH
        #
        # save_owner() consumes this value immediately.
        # Plaintext password is never stored.
        # -------------------------------------------------

        setattr(
            owner,
            "_password_hash",
            _hash_password(password),
        )

        return owner

    # =====================================================
    # 💾 SAVE OWNER
    # =====================================================

    def save_owner(
        self,
        owner: SupremeOwner,
    ) -> None:
        """
        Persist the SUPREME owner and credential hash.
        """

        if not isinstance(
            owner,
            SupremeOwner,
        ):
            raise TypeError(
                "owner must be SupremeOwner."
            )

        password_hash = getattr(
            owner,
            "_password_hash",
            None,
        )

        if not password_hash:
            raise ValueError(
                "Secure password hash is required "
                "when creating a SUPREME owner."
            )

        self.database.execute(
            """
            INSERT OR REPLACE INTO supreme_owner (

                master_id,
                supreme_id,
                owner_name,
                username,
                email,
                phone,
                role,
                level,
                status,
                two_factor_enabled,
                recovery_email,
                recovery_phone,
                dashboard_name,
                dashboard_theme,
                profile_visibility,
                system_version,
                created_at,
                updated_at

            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                owner.master_id,
                owner.supreme_id,
                owner.owner_name,
                owner.username,
                owner.email,
                owner.phone,
                owner.role.value,
                owner.level,
                owner.status,
                int(
                    owner.two_factor_enabled
                ),
                owner.recovery_email,
                owner.recovery_phone,
                owner.dashboard_name,
                owner.dashboard_theme,
                owner.profile_visibility.value,
                owner.system_version,
                owner.created_at,
                owner.updated_at,
            ),
        )

        self.database.execute(
            """
            INSERT OR REPLACE INTO supreme_credentials (

                supreme_id,
                password_hash,
                password_version,
                failed_attempts,
                locked,
                password_changed_at,
                created_at,
                updated_at

            )
            VALUES (
                ?, ?, ?, 0, 0, ?, ?, ?
            )
            """,
            (
                owner.supreme_id,
                password_hash,
                "PBKDF2-SHA256",
                owner.updated_at,
                owner.created_at,
                owner.updated_at,
            ),
        )

        # Remove temporary hash after persistence.
        try:
            delattr(
                owner,
                "_password_hash",
            )
        except AttributeError:
            pass

    # =====================================================
    # 👑 GET OWNER
    # =====================================================

    def get_owner(self) -> Any:
        """
        Return the SUPREME owner record.

        Credential data is never returned.
        """

        return self.database.fetchone(
            """
            SELECT
                id,
                master_id,
                supreme_id,
                owner_name,
                username,
                email,
                phone,
                role,
                level,
                status,
                two_factor_enabled,
                recovery_email,
                recovery_phone,
                dashboard_name,
                dashboard_theme,
                profile_visibility,
                system_version,
                created_at,
                updated_at
            FROM supreme_owner
            LIMIT 1
            """
        )

    # =====================================================
    # 👑 LIST OWNERS
    # =====================================================

    def list_owner(self) -> Any:
        """
        Return SUPREME owner records without credentials.
        """

        return self.database.fetchall(
            """
            SELECT
                id,
                master_id,
                supreme_id,
                owner_name,
                username,
                email,
                phone,
                role,
                level,
                status,
                two_factor_enabled,
                recovery_email,
                recovery_phone,
                dashboard_name,
                dashboard_theme,
                profile_visibility,
                system_version,
                created_at,
                updated_at
            FROM supreme_owner
            """
        )

    # =====================================================
    # 🔎 OWNER EXISTS
    # =====================================================

    def owner_exists(self) -> bool:
        """
        Check whether a SUPREME owner exists.
        """

        row = self.database.fetchone(
            """
            SELECT id
            FROM supreme_owner
            LIMIT 1
            """
        )

        return row is not None

    # =====================================================
    # ✏️ UPDATE OWNER
    # =====================================================

    def update_owner(
        self,
        owner: SupremeOwner,
    ) -> None:
        """
        Update SUPREME owner information.

        Credentials remain in the dedicated
        supreme_credentials table.
        """

        if not isinstance(
            owner,
            SupremeOwner,
        ):
            raise TypeError(
                "owner must be SupremeOwner."
            )

        self.database.execute(
            """
            UPDATE supreme_owner

            SET
                owner_name=?,
                username=?,
                email=?,
                phone=?,
                role=?,
                level=?,
                status=?,
                two_factor_enabled=?,
                recovery_email=?,
                recovery_phone=?,
                dashboard_name=?,
                dashboard_theme=?,
                profile_visibility=?,
                system_version=?,
                updated_at=?

            WHERE supreme_id=?
            """,
            (
                owner.owner_name,
                owner.username,
                owner.email,
                owner.phone,
                owner.role.value,
                owner.level,
                owner.status,
                int(
                    owner.two_factor_enabled
                ),
                owner.recovery_email,
                owner.recovery_phone,
                owner.dashboard_name,
                owner.dashboard_theme,
                owner.profile_visibility.value,
                owner.system_version,
                owner.updated_at,
                owner.supreme_id,
            ),
        )

    # =====================================================
    # 🗑️ DELETE OWNER
    # =====================================================

    def delete_owner(
        self,
        supreme_id: str,
    ) -> None:
        """
        Delete SUPREME owner and associated credentials.
        """

        if not supreme_id.strip():
            raise ValueError(
                "supreme_id cannot be empty."
            )

        self.database.execute(
            """
            DELETE FROM supreme_credentials
            WHERE supreme_id=?
            """,
            (supreme_id,),
        )

        self.database.execute(
            """
            DELETE FROM supreme_owner
            WHERE supreme_id=?
            """,
            (supreme_id,),
        )

    # =====================================================
    # 🔎 FIND OWNER BY IDENTIFIER
    # =====================================================

    def _find_owner_by_identifier(
        self,
        identifier: str,
    ) -> Any:
        """
        Find owner using username, email or phone.
        """

        if not isinstance(
            identifier,
            str,
        ):
            raise TypeError(
                "Identifier must be a string."
            )

        if not identifier.strip():
            raise ValueError(
                "Identifier cannot be empty."
            )

        return self.database.fetchone(
            """
            SELECT
                id,
                master_id,
                supreme_id,
                owner_name,
                username,
                email,
                phone,
                role,
                level,
                status,
                two_factor_enabled,
                recovery_email,
                recovery_phone,
                dashboard_name,
                dashboard_theme,
                profile_visibility,
                system_version,
                created_at,
                updated_at
            FROM supreme_owner
            WHERE username=?
               OR email=?
               OR phone=?
            LIMIT 1
            """,
            (
                identifier,
                identifier,
                identifier,
            ),
        )

    # =====================================================
    # 🔐 LOGIN LOOKUP
    # =====================================================

    def login(
        self,
        identifier: str,
    ) -> Any:
        """
        Locate the SUPREME owner account.

        IMPORTANT:
        This legacy method only resolves the identity.
        It does NOT claim successful password
        authentication because the existing controller
        accepts only an identifier.

        Full password verification is available through
        authenticate().
        """

        owner = self._find_owner_by_identifier(
            identifier
        )

        if owner is None:
            return {
                "authenticated": False,
                "status": "OWNER NOT FOUND",
            }

        return {
            "authenticated": False,
            "status": "IDENTITY FOUND",
            "authentication_required": True,
            "supreme_id": owner["supreme_id"],
            "username": owner["username"],
        }

    # =====================================================
    # 🔐 FULL AUTHENTICATION
    # =====================================================

    def authenticate(
        self,
        identifier: str,
        password: str,
    ) -> Dict[str, Any]:
        """
        Authenticate SUPREME owner using identifier
        and password.

        This method verifies the secure password hash.
        """

        owner = self._find_owner_by_identifier(
            identifier
        )

        if owner is None:
            return {
                "authenticated": False,
                "status": "INVALID CREDENTIALS",
            }

        if owner["status"] != "ACTIVE":
            return {
                "authenticated": False,
                "status": "ACCOUNT INACTIVE",
            }

        credential = self.database.fetchone(
            """
            SELECT
                password_hash,
                failed_attempts,
                locked
            FROM supreme_credentials
            WHERE supreme_id=?
            LIMIT 1
            """,
            (
                owner["supreme_id"],
            ),
        )

        if credential is None:
            return {
                "authenticated": False,
                "status": "CREDENTIALS NOT CONFIGURED",
            }

        if credential["locked"]:
            return {
                "authenticated": False,
                "status": "ACCOUNT LOCKED",
            }

        valid = _verify_password(
            password,
            credential["password_hash"],
        )

        if not valid:

            failed_attempts = (
                credential["failed_attempts"]
                + 1
            )

            locked = (
                1
                if failed_attempts >= 5
                else 0
            )

            self.database.execute(
                """
                UPDATE supreme_credentials

                SET
                    failed_attempts=?,
                    locked=?,
                    updated_at=datetime('now')

                WHERE supreme_id=?
                """,
                (
                    failed_attempts,
                    locked,
                    owner["supreme_id"],
                ),
            )

            return {
                "authenticated": False,
                "status": (
                    "ACCOUNT LOCKED"
                    if locked
                    else "INVALID CREDENTIALS"
                ),
            }

        self.database.execute(
            """
            UPDATE supreme_credentials

            SET
                failed_attempts=0,
                locked=0,
                last_login_at=datetime('now'),
                updated_at=datetime('now')

            WHERE supreme_id=?
            """,
            (
                owner["supreme_id"],
            ),
        )

        return {
            "authenticated": True,
            "status": "AUTHENTICATED",
            "supreme_id": owner["supreme_id"],
            "username": owner["username"],
            "role": owner["role"],
            "level": owner["level"],
            "profile_visibility": (
                "OWNER_ONLY"
            ),
        }

    # =====================================================
    # 🔓 LOGOUT
    # =====================================================

    def logout(self) -> Dict[str, str]:
        """
        End the application-level SUPREME session.

        Actual token/session invalidation belongs to the
        authentication/session layer.
        """

        return {
            "status": "LOGOUT SUCCESS"
        }

    # =====================================================
    # 🔑 CHANGE PASSWORD
    # =====================================================

    def change_password(
        self,
        supreme_id: str,
        password: str,
    ) -> Dict[str, str]:
        """
        Change the SUPREME owner password.

        The password is securely hashed before storage.
        """

        if not supreme_id.strip():
            raise ValueError(
                "supreme_id cannot be empty."
            )

        if not password:
            raise ValueError(
                "Password cannot be empty."
            )

        password_hash = _hash_password(
            password
        )

        self.database.execute(
            """
            UPDATE supreme_credentials

            SET
                password_hash=?,
                password_version=?,
                failed_attempts=0,
                locked=0,
                password_changed_at=datetime('now'),
                updated_at=datetime('now')

            WHERE supreme_id=?
            """,
            (
                password_hash,
                "PBKDF2-SHA256",
                supreme_id,
            ),
        )

        return {
            "status": "PASSWORD UPDATED"
        }

    # =====================================================
    # 📊 STATUS
    # =====================================================

    def status(self) -> Dict[str, Any]:
        """
        Return SUPREME service status.
        """

        return {
            "service": "SUPREME",
            "initialized": self._initialized,
            "owner_exists": self.owner_exists(),
            "password_storage": "PBKDF2-SHA256",
            "profile_visibility": "OWNER_ONLY",
        }


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "SupremeService",
]
