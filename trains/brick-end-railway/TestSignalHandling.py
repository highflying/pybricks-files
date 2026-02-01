from pybricks.hubs import CityHub
from pybricks.pupdevices import Remote, DCMotor, ColorDistanceSensor
from pybricks.parameters import Button, Port, Color
from pybricks.tools import wait

from uerrno import ENODEV, ETIMEDOUT

# teal
min_h = 170
max_h = 195
min_s = 90
max_s = 100
min_v = 60
max_v = 76

stop_interval = 5000
continue_interval = 2000
hub_name = 'bercont'
controller_timeout = 30000
default_power = 30

debug_colour = False

class TrainHub(object):
    def __init__(self):
        self._hub = CityHub(observe_channels=[1])
        # self._remote = Remote(name=hub_name, timeout=controller_timeout)    
        # self._remote = Remote(timeout=controller_timeout)       
        # self._remote.name(hub_name)
        self.connect_remote()
        self._hub.light.on(Color.GREEN)
        self._motor = DCMotor(Port.A)
        self.has_sensor = False
        self.position = 0
        # self.timer = StopWatch()
        
        try:
            self._sensor = ColorDistanceSensor(Port.B)
            self.has_sensor = True
        except OSError as ex:
            if ex.errno == ENODEV:
                print('No colour sensor')
            else:
                raise RuntimeError

        self.power = default_power
        self.stop()
        # self.remote_connected = True
    
    def connect_remote(self, tout=30000):
        try:
            self._remote = Remote(name=hub_name, timeout=tout)
            self.remote_connected = True
            self._hub.light.on(Color.YELLOW)
        except OSError as ex:
            if ex.errno == ETIMEDOUT:
                print('Unable to reconnect to remote')
                self.remote_connected = False
            else:
                raise RuntimeError

    def set_led_colour(self, led_colour):


        try:
            self._remote.light.on(led_colour)
        except OSError as ex:
            if ex.errno == ENODEV:
                print('Remote disconnected')
                self.remote_connected = False
                # self.connect_remote(500)
            else:
                print(ex)
                raise RuntimeError

        if self.remote_connected:
            self._hub.light.on(led_colour)
        else:
            self._hub.light.on(Color.BLUE)
    
    # def move_forward(self):
    #     # self.power = 40
    #     self.start()

    # def move_backward(self):
    #     # self.power = -40
    #     self.power = self.power * -1
    #     self.start()

    def stop(self):
        self._motor.stop()
        self.running = False
        self.set_led_colour(Color.RED)
        self._hub.ble.broadcast(0)
    
    def start(self):
        self._motor.dc(self.power)
        self.running = True
        self.set_led_colour(Color.GREEN)
        wait(continue_interval)
        self._hub.ble.broadcast(1)

    # def pause_at_station(self):
    #     self.stop()
    #     wait(stop_interval)
    #     self.start()
    #     wait(continue_interval)

    # def reverse_direction(self):
    #     self.power = self.power * -1

    def controller(self):
        try:
            pressed = self._remote.buttons.pressed()
        except OSError as ex:
            if ex.errno == ENODEV:
                # print('Remote disconnected, will try to reconnect')
                pressed = {}
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
        elif Button.RIGHT_MINUS in pressed:
            if self.power > -100:
                self.power = self.power - 10
        elif Button.RIGHT in pressed:
            self.stop()
        elif not self.remote_connected:
            if not self.running:
                wait(1000)
                self.start()

    def sensor(self):
        if not self.running:
            return

        if self.has_sensor:
            colour = self._sensor.hsv()

            if debug_colour:
                print(colour)

            if ( colour.h >= min_h and colour.h <= max_h 
                and colour.s >= min_s and colour.s <= max_s 
                and colour.v >= min_v and colour.v <= max_v ):

                self.stop()



train = TrainHub()

print('running')

while True:
    train.controller()
    train.sensor()
#     train.run()

    wait(50)
