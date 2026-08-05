class BaseEngine:

    def __init__(self, name: str):
        self.name = name
        self.state = "STOPPED"

    def load(self):
        self.state = "LOADED"

    def unload(self):
        self.state = "UNLOADED"

    def start(self):
        self.state = "RUNNING"

    def stop(self):
        self.state = "STOPPED"

    def restart(self):
        self.stop()
        self.start()

    def status(self):
        return {
            "engine": self.name,
            "state": self.state
        }
