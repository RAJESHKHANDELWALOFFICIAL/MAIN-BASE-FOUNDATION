    def status(self) -> dict:
        """Return the current connectivity status."""

        return self.engine.detect()
