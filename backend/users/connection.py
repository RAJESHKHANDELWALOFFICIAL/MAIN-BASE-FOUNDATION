from backend.database.connection import DatabaseConnection


class UserConnection:

    def __init__(self):
        self.database = DatabaseConnection().connect()

    def connect(self):
        return self.database
