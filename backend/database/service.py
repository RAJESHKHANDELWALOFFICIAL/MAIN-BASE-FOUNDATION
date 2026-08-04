from backend.database.connection import DatabaseConnection


class DatabaseService:

    def __init__(self):
        self.connection = DatabaseConnection()

    def initialize(self):
        return self.connection.connect()
