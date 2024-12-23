from pybricks.pupdevices import DCMotor
from pybricks.parameters import Port


class TrainMotor:
    current_power = 0
    slow_power = 0
    fast_power = 0
    direction = 1

    def __init__(self, slow_power, fast_power):
        self.motor = DCMotor(Port.A)
        self.slow_power = slow_power
        self.fast_power = fast_power

    def toggle_direction(self):
        self.direction *= -1

    def stop(self):
        self.current_power = 0
        self.motor.stop()

    def slow(self):
        self.current_power = self.slow_power * self.direction
        self.motor.dc(self.current_power)

    def fast(self):
        self.current_power = self.fast_power * self.direction
        self.motor.dc(self.current_power)

    def is_stopped(self):
        return self.current_power == 0

    def is_reversing(self):
        return self.current_power == self.slow_power * -1

    def is_slow(self):
        return self.current_power == self.slow_power
