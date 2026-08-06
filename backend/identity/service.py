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
        
