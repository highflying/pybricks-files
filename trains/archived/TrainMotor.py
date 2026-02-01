from pybricks.pupdevices import DCMotor
from pybricks.parameters import Port


class TrainMotor:
    current_power = 0
    slow_power = 0
    fast_power = 0

    def __init__(self, slow_power, fast_power):
        self.motor = DCMotor(Port.A)
        self.slow_power = slow_power
        self.fast_power = fast_power

    def stop(self):
        self.current_power = 0
        self.motor.stop()

    def slow(self):
        self.current_power = self.slow_power
        self.motor.dc(self.current_power)

    def fast(self):
        self.current_power = self.fast_power
        self.motor.dc(self.current_power)

    def reverse(self):
        self.current_power = self.slow_power * -1
        self.motor.dc(self.current_power)

    def is_stopped(self):
        return self.current_power == 0

    def is_reversing(self):
        return self.current_power == self.slow_power * -1

    def is_slow(self):
        return self.current_power == self.slow_power
