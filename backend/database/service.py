from backend.database.connection import DatabaseConnection


class DatabaseService:

    def __init__(self):
        self.connection = DatabaseConnection().connect()

    def initialize(self):

        cursor = self.connection.cursor()

        # ==========================
        # SYSTEM INFO
        # ==========================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_info (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            foundation TEXT,
            version TEXT

        )
        """)

        # ==========================
        # MASTER IDENTITY
        # ==========================

        cursor.execute("""
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

        # ==========================
        # SUPREME OWNER
        # ==========================

        cursor.execute("""
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

        self.connection.commit()

        return {
            "database": "SQLite",
            "status": "Initialized"
        }

    def execute(self, query, parameters=()):
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        self.connection.commit()
        return cursor

    def fetchone(self, query, parameters=()):
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchone()

    def fetchall(self, query, parameters=()):
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()

    def cursor(self):
        return self.connection.cursor()

    def health(self):
        return {
            "database": "SQLite",
            "status": "CONNECTED"
        }
