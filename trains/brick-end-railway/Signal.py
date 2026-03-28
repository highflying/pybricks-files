from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait

class Signal(object):
    def __init__(self, port):
        self._motor = Motor(port)
        self.power = 90
        self.go = True
        self.calibrate()

    def calibrate(self):
        self._motor.run_until_stalled(20, Stop.COAST, 20)
        wait(500)
        self.min = self._motor.angle()
        self._motor.run_until_stalled(-20, Stop.COAST, 20)
        wait(500)
        self.max = self._motor.angle()
        wait(2000)

    def set_go(self):
        if self.go:
            return

        self._motor.run_target(self.power, self.max)
        self.go = True


    def set_stop(self):
        if not self.go:
            return
            
        self._motor.run_target(self.power, self.min)
        self.go = False

