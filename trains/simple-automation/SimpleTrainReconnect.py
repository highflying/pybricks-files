from pybricks.hubs import CityHub
from pybricks.pupdevices import Remote, DCMotor, ColorDistanceSensor
from pybricks.parameters import Button, Port, Color
from pybricks.tools import wait
from uerrno import ENODEV, ETIMEDOUT

# Teal
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
controller_timeout = 10000

debug_colour = False

class TrainHub(object):
    def __init__(self):
        self._hub = CityHub()
        self._remote = None
        self.connect_remote()

        self._motor = DCMotor(Port.A)
        self.has_sensor = False
        self.position = 0
        self.stop_at_station = False

        try:
            self._sensor = ColorDistanceSensor(Port.B)
            self.has_sensor = True
        except OSError as ex:
            if ex.errno == ENODEV:
                print('No colour sensor')
            else:
                raise RuntimeError

        self.power = 0
        if self.remote_connected:
            self.stop()
        else:
            self.start()

    def connect_remote(self):
        try:
            self._remote = Remote(name=hub_name, timeout=controller_timeout)
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
    
    def set_led_colour(self, led_colour):
        self._hub.light.on(led_colour)
        try:
            if self._remote is not None:
                self._remote.light.on(led_colour)
        except OSError as ex:
            if ex.errno == ENODEV:
                self.remote_connected = False
            else:
                raise RuntimeError

    def stop(self):
        self._motor.stop()
        self.set_led_colour(Color.RED)

    
    def start(self):
        self._motor.dc(self.power)
        if self.power > 0:
            self.set_led_colour(Color.GREEN)
        elif self.power == 0:
            self.set_led_colour(Color.RED)
        else:
            self.set_led_colour(Color.BLUE)

    def pause_at_station(self):
        self.stop()
        wait(stop_interval)
        self.start()
        if not self.remote_connected:
            self.connect_remote()
        else:
            wait(continue_interval)

    def run(self):
        if self.remote_connected:
            try:
                if self._remote is not None:
                    pressed = self._remote.buttons.pressed()
                    
                    if Button.LEFT_PLUS in pressed:
                        self.stop_at_station = True
                        if self.power < 100:
                            self.power = self.power + 10
                        self.start()
                    elif Button.LEFT_MINUS in pressed:
                        self.stop_at_station = True
                        if self.power > -100:
                            self.power = self.power - 10
                        self.start()
                    elif Button.LEFT in pressed or Button.RIGHT in pressed:
                        self.power = 0
                        self.stop()
                    elif Button.RIGHT_PLUS in pressed:
                        self.stop_at_station = False
                        if self.power < 100:
                            self.power = self.power + 10
                        self.start()
                    elif Button.RIGHT_MINUS in pressed:
                        self.stop_at_station = False
                        if self.power > -100:
                            self.power = self.power - 10
                        self.start()

            except OSError as ex:
                if ex.errno == ENODEV:
                    self.remote_connected = False
                else:
                    raise RuntimeError

        if self.has_sensor and self.stop_at_station:
            colour = self._sensor.hsv()

            if debug_colour:
                print(colour)

            if ( colour.h >= SensorColour.min_h
                and colour.h <= SensorColour.max_h 
                and colour.s >= SensorColour.min_s
                and colour.s <= SensorColour.max_s 
                and colour.v >= SensorColour.min_v
                and colour.v <= SensorColour.max_v ):

                self.position = self.position + 1

                if self.position == 1:
                    self.pause_at_station()
                    self.position = 0


train = TrainHub()

while True:
    train.run()

    wait(100)
