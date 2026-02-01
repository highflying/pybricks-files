from pybricks.pupdevices import ColorDistanceSensor
from pybricks.parameters import Port

DETECT_DISTANCE = 80


class DistanceSensor:
    sensor_off = False

    def __init__(self, port=Port.D):
        self.sensor = ColorDistanceSensor(port)

    def is_triggered(self):
        self.sensor_off = False
        distance = self.sensor.distance()

        if distance < DETECT_DISTANCE:
            self.off()
            return True

        return False

    def off(self):
        if self.sensor_off:
            return

        self.sensor.light.off()
        self.sensor_off = True
