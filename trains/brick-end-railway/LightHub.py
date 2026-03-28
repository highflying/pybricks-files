from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Color, Button
from pybricks.tools import wait, StopWatch
from uerrno import ENODEV, ETIMEDOUT

from Channels import Channels
from Messages import Messages
from Light import LightController

class LightHub(object):
    def __init__(self, remote_name):
        self.remote_name = remote_name

        self._hub = TechnicHub()

        self.connect_remote()

        self.light = LightController(Port.A)
        self.power = 90
        self._hub.light.on(Color.GREEN)

    def connect_remote(self, tout=30000):
        try:
            self._remote = Remote(name=self.remote_name, timeout=tout)
            self.remote_connected = True
            self._hub.light.on(Color.GREEN)
            self._remote.light.on(Color.GREEN)
        except OSError as ex:
            if ex.errno == ETIMEDOUT:
                print('Unable to reconnect to remote')
                self.remote_connected = False
                self._hub.light.on(Color.RED)
            else:
                print(ex)
                raise RuntimeError

    def controller(self):
        try:
            pressed = self._remote.buttons.pressed()
        except OSError as ex:
            if ex.errno == ENODEV:
                pressed = {}
                self.connect_remote(1000)
            else:
                raise RuntimeError

        if Button.LEFT in pressed:
            self.light.ghost_on()
        else:
            self.light.ghost_off()
        # elif Button.RIGHT in pressed:
        #     self.point.set_divergent()

        # if self.point.straight:
        #     self._hub.ble.broadcast(Messages.Straight)
        # else:
        #     self._hub.ble.broadcast(Messages.Divergent)



