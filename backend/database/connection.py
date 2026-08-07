import sqlite3


class DatabaseConnection:

    def __init__(self):

        self.database_name = "main_base_foundation.db"
        self.connection = None

    def connect(self):

        if self.connection is None:

            self.connection = sqlite3.connect(
                self.database_name,
                check_same_thread=False
            )

            self.connection.row_factory = sqlite3.Row

        return self.connection

    def close(self):

        if self.connection is not None:

            self.connection.close()
            self.connection = None

    def is_connected(self):

        return self.connection is not None

    def database(self):

        return self.database_name
