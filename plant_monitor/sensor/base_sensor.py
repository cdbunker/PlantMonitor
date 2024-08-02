class BaseSensor:
    def __init__(self):
        pass

    def read(self):
        raise NotImplementedError("Subclasses should implement this!")
