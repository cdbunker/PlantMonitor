from .base_sensor import BaseSensor


class BaseTemperatureSensor(BaseSensor):
    def read_temperature(self):
        raise NotImplementedError("Subclasses should implement this!")
