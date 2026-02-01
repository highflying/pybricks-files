from pybricks.hubs import CityHub
from pybricks.pupdevices import Remote, DCMotor, ColorDistanceSensor
from pybricks.parameters import Button, Port, Color
from pybricks.tools import wait, StopWatch
from uerrno import ENODEV, ETIMEDOUT

from Channels import Channels
from Messages import Messages

class SensorColour:
    min_h = 170
    max_h = 200
    min_s = 80
    max_s = 100
    min_v = 50
    max_v = 76

stop_interval = 5000
continue_interval = 2000
hub_name = 'bercont'
controller_timeout = 30000
default_power = 60

debug_colour = True

class TrainHub(object):
    def __init__(self):
        self._hub = CityHub(broadcast_channel=Channels.LoopTrain)
        self.connect_remote()
        self.direction = Messages.Forward
        self._motor = DCMotor(Port.A)
        self.timer = StopWatch()
        self._sensor = ColorDistanceSensor(Port.B)
        self.power = default_power
        self.stop_timer = StopWatch()
        self.stop()
    
    def connect_remote(self, tout=30000):
        try:
            self._remote = Remote(name=hub_name, timeout=tout)
            self.remote_connected = True
            self._hub.light.on(Color.GREEN)
            self._remote.light.on(Color.GREEN)
        except OSError as ex:
            if ex.errno == ETIMEDOUT:
                print('Unable to reconnect to remote')
                self.remote_connected = False
                self._hub.light.on(Color.RED)
            else:
                raise RuntimeError

    def set_led_colour(self):
        try:
            self._remote.light.on(Color.GREEN)
        except OSError as ex:
            if ex.errno == ENODEV:
                self.remote_connected = False
            else:
                print(ex)
                raise RuntimeError

        if self.remote_connected:
            self._hub.light.on(Color.GREEN)
        else:
            self._hub.light.on(Color.RED)

    def stop(self):
        self._motor.stop()
        self.running = False
        self._hub.ble.broadcast(Messages.Stopped)
        for _ in range(10):
            wait(100)
            self._hub.ble.broadcast(Messages.Stopped)

    def start(self):
        self._hub.ble.broadcast(self.direction)
        for _ in range(20):
            wait(100)
            self._hub.ble.broadcast(self.direction)
        if self.direction == Messages.Forward:
            self._motor.dc(self.power)
        else:
            self._motor.dc(self.power * -1)

        self.running = True
        self.timer.reset()
        self.timer.resume()

    def controller(self):
        pressed = {}
        try:
            pressed = self._remote.buttons.pressed()
        except OSError as ex:
            if ex.errno == ENODEV:
                # pressed = {}
                if not self.running:
                    self.connect_remote(1000)
            else:
                raise RuntimeError

        if Button.LEFT in pressed:
            if not self.running:
                self.start()
        elif Button.RIGHT_PLUS in pressed:
            if self.power < 100:
                self.power = self.power + 10
                if self.running:
                    if self.direction == Messages.Forward:
                        self._motor.dc(self.power)
                    else:
                        self._motor.dc(self.power * -1)
                    wait(1000)
        elif Button.RIGHT_MINUS in pressed:
            if self.power > 0:
                self.power = self.power - 10
                if self.running:
                    if self.direction == Messages.Forward:
                        self._motor.dc(self.power)
                    else:
                        self._motor.dc(self.power * -1)
                    wait(1000)
        elif Button.RIGHT in pressed:
            self.stop()
        elif not self.remote_connected:
            if not self.running:
                wait(1000)
                self.start()

    def sensor(self):
        if not self.running:
            return

        if self.timer.time() < continue_interval:
            return

        colour = self._sensor.hsv()

        if debug_colour:
            print(colour)

        if ( colour.h >= SensorColour.min_h
            and colour.h <= SensorColour.max_h 
            and colour.s >= SensorColour.min_s
            and colour.s <= SensorColour.max_s 
            and colour.v >= SensorColour.min_v
            and colour.v <= SensorColour.max_v ):

            self.stop()

train = TrainHub()

while True:
    train.controller()
    train.sensor()

    if train.running:
        train._hub.ble.broadcast(train.direction)
    else:
        train._hub.ble.broadcast(Messages.Stopped)

    wait(50)
