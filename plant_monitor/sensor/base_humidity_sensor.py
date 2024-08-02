from .base_sensor import BaseSensor


class BaseHumiditySensor(BaseSensor):
    def read_humidity(self):
        raise NotImplementedError("Subclasses should implement this!")
