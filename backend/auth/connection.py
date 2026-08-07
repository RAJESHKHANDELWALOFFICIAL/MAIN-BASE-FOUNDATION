from backend.database.connection import DatabaseConnection


class AuthenticationConnection:

    def __init__(self):

        self.connection = DatabaseConnection().connect()

    def connect(self):

        return self.connection

    def cursor(self):

        return self.connection.cursor()

    def commit(self):

        self.connection.commit()

    def rollback(self):

        self.connection.rollback()

    def close(self):

        self.connection.close()

    def health(self):

        return {
            "authentication": "CONNECTED"
        }
