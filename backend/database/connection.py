import sqlite3


class DatabaseConnection:

    def __init__(self):
        self.database_name = "main_base_foundation.db"

    def connect(self):
        connection = sqlite3.connect(self.database_name)
        return connection
