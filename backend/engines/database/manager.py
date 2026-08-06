from backend.engines.base import BaseEngine


class DatabaseEngine(BaseEngine):

    def __init__(self):
        super().__init__("Database Engine")
