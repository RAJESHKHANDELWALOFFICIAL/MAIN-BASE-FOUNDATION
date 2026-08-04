from backend.core.bootstrap import Bootstrap


class FoundationManager:

    def start(self):
        bootstrap = Bootstrap()
        return bootstrap.boot()
