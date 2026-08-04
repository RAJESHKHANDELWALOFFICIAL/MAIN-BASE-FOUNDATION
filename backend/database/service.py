from backend.database.connection import DatabaseConnection


class DatabaseService:

    def __init__(self):
        self.connection = DatabaseConnection().connect()

    def initialize(self):
        cursor = self.connection.cursor()

        # System Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            foundation TEXT,
            version TEXT
        )
        """)

        # Master Identity Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_identity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            master_id TEXT UNIQUE,
            full_name TEXT,
            display_name TEXT,
            username TEXT,
            email TEXT,
            phone TEXT,
            status TEXT
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
