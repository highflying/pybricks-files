from pybricks.pupdevices import Motor
from pybricks.tools import wait

class Point(object):
    def __init__(self, port):
        self._motor = Motor(port)
        self.power = 180
        self.straight = True
        self.calibrate()

    def calibrate(self):
        self._motor.run_until_stalled(70)
        wait(500)
        self.min = self._motor.angle()
        self._motor.run_until_stalled(-70)
        wait(500)
        self.max = self._motor.angle()
        wait(2000)

    def set_straight(self):
        if self.straight:
            return

        self._motor.run_target(self.power, self.max)
        self.straight = True


    def set_divergent(self):
        if not self.straight:
            return
            
        self._motor.run_target(self.power, self.min)
        self.straight = False

