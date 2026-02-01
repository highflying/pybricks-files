from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Remote, Motor
from pybricks.parameters import Button, Port
from pybricks.tools import wait

class WindmillHub(object):
    def __init__(self):
        self._hub = TechnicHub()
        self._remote = Remote(name="windmill", timeout=30000)       
        self._motor = Motor(Port.A)

    def run(self):
        pressed = self._remote.buttons.pressed()

        if Button.LEFT in pressed:
            self._motor.dc(-20)
            wait(10000)
            self._motor.dc(-15)
            wait(1000)
            self._motor.stop()

windmill = WindmillHub()

while True:
    windmill.run()

    wait(10)
