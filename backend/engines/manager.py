from typing import Dict, Any


class EngineManager:

    def __init__(self):
        self.engines: Dict[str, Any] = {}

    def register_engine(self, name: str, engine: Any):
        """
        Register a new engine.
        """
        self.engines[name] = engine
        return True

    def unregister_engine(self, name: str):
        """
        Remove an engine.
        """
        if name in self.engines:
            del self.engines[name]
            return True
        return False

    def load_engine(self, name: str):
        """
        Load an engine.
        """
        engine = self.engines.get(name)

        if engine and hasattr(engine, "load"):
            return engine.load()

        return None

    def unload_engine(self, name: str):
        """
        Unload an engine.
        """
        engine = self.engines.get(name)

        if engine and hasattr(engine, "unload"):
            return engine.unload()

        return None

    def start_all(self):
        """
        Start all registered engines.
        """
        for engine in self.engines.values():
            if hasattr(engine, "start"):
                engine.start()

    def stop_all(self):
        """
        Stop all registered engines.
        """
        for engine in self.engines.values():
            if hasattr(engine, "stop"):
                engine.stop()

    def restart_engine(self, name: str):
        """
        Restart a single engine.
        """
        engine = self.engines.get(name)

        if engine:
            if hasattr(engine, "stop"):
                engine.stop()

            if hasattr(engine, "start"):
                engine.start()

    def get_engine(self, name: str):
        """
        Get engine instance.
        """
        return self.engines.get(name)

    def list_engines(self):
        """
        List all registered engines.
        """
        return list(self.engines.keys())

    def engine_status(self):
        """
        Return status of every engine.
        """
        status = {}

        for name, engine in self.engines.items():

            if hasattr(engine, "status"):
                status[name] = engine.status()

            else:
                status[name] = "UNKNOWN"

        return status
