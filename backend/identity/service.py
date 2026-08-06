from backend.identity.model import MasterIdentity
from backend.database.service import DatabaseService
from backend.identity.generator import IdentityGenerator
from backend.identity.validator import IdentityValidator


class IdentityService:

    def __init__(self):

        self.database = DatabaseService()
        self.generator = IdentityGenerator()
        self.validator = IdentityValidator()

    def initialize(self):

        self.database.initialize()

        self.database.execute("""
        CREATE TABLE IF NOT EXISTS master_identity (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            master_id TEXT UNIQUE,
            identity_id TEXT UNIQUE,
            supreme_id TEXT,

            full_name TEXT,
            display_name TEXT,
            username TEXT UNIQUE,

            email TEXT,
            phone TEXT,

            country TEXT,
            state TEXT,
            city TEXT,

            language TEXT,
            timezone TEXT,

            status TEXT,
            verified INTEGER,

            profile_photo TEXT,
            profile_type TEXT,

            version TEXT,

            created_at TEXT,
            updated_at TEXT

        )
        """)

        return {
            "identity": "Initialized",
            "status": "READY"
        }

    def create_identity(
        self,
        supreme_id,
        full_name,
        display_name,
        username,
        email,
        phone,
        country="",
        state="",
        city=""
    ):

        if not self.validator.validate_username(username):
            raise ValueError("Invalid Username")

        if not self.validator.validate_email(email):
            raise ValueError("Invalid Email")

        if not self.validator.validate_phone(phone):
            raise ValueError("Invalid Phone")

        return MasterIdentity(
            master_id=self.generator.generate_master_id(),
            identity_id=self.generator.generate_identity_id(),
            supreme_id=supreme_id,
            full_name=full_name,
            display_name=display_name,
            username=username,
            email=email,
            phone=phone,
            country=country,
            state=state,
            city=city
        )

    def save_identity(self, identity):

        self.database.execute(
            """
            INSERT INTO master_identity (

                master_id,
                identity_id,
                supreme_id,
                full_name,
                display_name,
                username,
                email,
                phone,
                country,
                state,
                city,
                language,
                timezone,
                status,
                verified,
                profile_photo,
                profile_type,
                version,
                created_at,
                updated_at

            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                identity.master_id,
                identity.identity_id,
                identity.supreme_id,
                identity.full_name,
                identity.display_name,
                identity.username,
                identity.email,
                identity.phone,
                identity.country,
                identity.state,
                identity.city,
                identity.language,
                identity.timezone,
                identity.status,
                int(identity.verified),
                identity.profile_photo,
                identity.profile_type,
                identity.version,
                identity.created_at,
                identity.updated_at,
            ),
        )

    
    def get_identity(self, master_id):

        row = self.database.fetchone(
            """
            SELECT *
            FROM master_identity
            WHERE master_id = ?
            """,
            (master_id,),
        )

        if row is None:
            return None

        return MasterIdentity(
            id=row[0],
            master_id=row[1],
            identity_id=row[2],
            supreme_id=row[3],
            full_name=row[4],
            display_name=row[5],
            username=row[6],
            email=row[7],
            phone=row[8],
            country=row[9],
            state=row[10],
            city=row[11],
            language=row[12],
            timezone=row[13],
            status=row[14],
            verified=bool(row[15]),
            profile_photo=row[16],
            profile_type=row[17],
            version=row[18],
            created_at=row[19],
            updated_at=row[20],
        )

    def list_identity(self):

        rows = self.database.fetchall(
            """
            SELECT *
            FROM master_identity
            """
        )

        identities = []

        for row in rows:

            identities.append(
                MasterIdentity(
                    id=row[0],
                    master_id=row[1],
                    identity_id=row[2],
                    supreme_id=row[3],
                    full_name=row[4],
                    display_name=row[5],
                    username=row[6],
                    email=row[7],
                    phone=row[8],
                    country=row[9],
                    state=row[10],
                    city=row[11],
                    language=row[12],
                    timezone=row[13],
                    status=row[14],
                    verified=bool(row[15]),
                    profile_photo=row[16],
                    profile_type=row[17],
                    version=row[18],
                    created_at=row[19],
                    updated_at=row[20],
                )
            )

        return identities
        
    def update_identity(self, identity):

        self.database.execute(
            """
            UPDATE master_identity
            SET

                full_name = ?,
                display_name = ?,
                username = ?,
                email = ?,
                phone = ?,
                country = ?,
                state = ?,
                city = ?,
                language = ?,
                timezone = ?,
                status = ?,
                verified = ?,
                profile_photo = ?,
                profile_type = ?,
                version = ?,
                updated_at = ?

            WHERE master_id = ?
            """,
            (
                identity.full_name,
                identity.display_name,
                identity.username,
                identity.email,
                identity.phone,
                identity.country,
                identity.state,
                identity.city,
                identity.language,
                identity.timezone,
                identity.status,
                int(identity.verified),
                identity.profile_photo,
                identity.profile_type,
                identity.version,
                identity.updated_at,
                identity.master_id,
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
        
    def search_identity(self, keyword):

        return self.database.fetchall(
            """
            SELECT *
            FROM master_identity
            WHERE
                master_id = ?
                OR identity_id = ?
                OR username = ?
                OR email = ?
                OR phone = ?
                OR full_name LIKE ?
                OR display_name LIKE ?
            """,
            (
                keyword,
                keyword,
                keyword,
                keyword,
                keyword,
                f"%{keyword}%",
                f"%{keyword}%"
            ),
        )

    def identity_exists(self, master_id):

        row = self.database.fetchone(
            """
            SELECT id
            FROM master_identity
            WHERE master_id = ?
            """,
            (master_id,),
        )

        return row is not None

    def verify_identity(self, master_id):

        self.database.execute(
            """
            UPDATE master_identity
            SET
                verified = 1
            WHERE master_id = ?
            """,
            (master_id,),
        )

        return {
            "status": "IDENTITY VERIFIED"
        }
        
