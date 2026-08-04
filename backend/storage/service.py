from backend.storage.connection import StorageConnection


class StorageService:

    def __init__(self):
        self.connection = StorageConnection()

    def initialize(self):
        return self.connection.connect()
