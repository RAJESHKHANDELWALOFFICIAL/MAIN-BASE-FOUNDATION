from backend.database.connection import DatabaseConnection


class DatabaseService:

    def __init__(self):
        self.connection = DatabaseConnection().connect()

    def initialize(self):
        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            foundation TEXT,
            version TEXT
        )
        """)

        self.connection.commit()

        return {
            "database": "SQLite",
            "status": "Initialized"
        }
