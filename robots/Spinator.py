from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Light, Remote, DCMotor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.iodevices import PUPDevice
from uerrno import ENODEV
from pybricks.tools import wait

class TrainHub(object):
    def __init__(self):
        self._device_names = {
            # pybricks.pupdevices.DCMotor
            1: "Wedo 2.0 Medium Motor",
            2: "Powered Up Train Motor",
            # pybricks.pupdevices.Motor
            46: "Technic Large Motor",
            47: "Technic Extra Large Motor"
        }
        self._hub = TechnicHub()
        self._remote = Remote(timeout=30000)
        self._ports = [Port.A, Port.B]
        self._spin_power = 0
        self._buttons_pressed = {Button.LEFT: 0 ,Button.LEFT_PLUS: 0, Button.LEFT_MINUS: 0, Button.RIGHT: 0, Button.RIGHT_MINUS: 0, Button.RIGHT_PLUS: 0, Button.CENTER: 0}
        self.setup()

    def setup(self):
        for port in self._ports:

            # Try to get the device, if it is attached.
            try:
                device = PUPDevice(port)
            except OSError as ex:
                if ex.args[0] == ENODEV:
                    continue
                else:
                    raise

            # Get the device id
            id = device.info()["id"]

            if id == 1 or id == 2 or id == 46 or id == 47:
                if port == Port.A:
                    self._left_motor = TrainMotor(port, id)
                elif port == Port.B:
                    self._right_motor = TrainMotor(port, id)

    # def button_pressed(self, port):
    #     if self._devices[port] is not None:
    #         self._devices[port].stop()

    # def up_button_pressed(self, port):
    #     if self._devices[port] is not None:
    #         self._devices[port].increase_power()

    # def down_button_pressed(self, port):
    #     if self._devices[port] is not None:
    #         self._devices[port].decrease_power()

    def run(self):
        pressed = self._remote.buttons.pressed()

        # for button in self._buttons_pressed.keys():
        #     if button in pressed:
        #         self._buttons_pressed[button] += 1
        #     else:
        #         self._buttons_pressed[button] = 0

        # Check a specific button.
        if Button.LEFT in pressed:
            self._left_motor.stop()
            self._right_motor.stop()
            self._spin_power = 0
            self._hub.light.on(Color.RED)
        elif Button.LEFT_UP in pressed:
            if self._spin_power != 0:
                self._left_motor.set_power(self._spin_power)
                self._right_motor.set_power(self._spin_power)
            self._hub.light.on(Color.GREEN)
        elif Button.LEFT_PLUS in pressed:
            self._left_motor.set_power(100)
            self._right_motor.set_power(-100)
            self._hub.light.on(Color.BLUE)
        elif Button.LEFT_MINUS in pressed:
            self._left_motor.set_power(-100)
            self._right_motor.set_power(100)
            self._hub.light.on(Color.YELLOW)
    
        # elif self._buttons_pressed[Button.LEFT_MINUS] == 20:
        #     if self._spin_power != 0:
        #         self._left_motor.set_power(self._spin_power)
        #         self._right_motor.set_power(self._spin_power)

        if Button.RIGHT in pressed:
            self._left_motor.stop()
            self._right_motor.stop()
            self._hub.light.on(Color.RED)
        elif Button.RIGHT_PLUS in pressed:
            self._left_motor.set_power(100)
            self._right_motor.set_power(100)
            self._spin_power = 100
            self._hub.light.on(Color.VIOLET)
        elif Button.RIGHT_MINUS in pressed:
            self._left_motor.set_power(-100)
            self._right_motor.set_power(-100)
            self._spin_power = -100
            self._hub.light.on(Color.WHITE)
        # elif self._buttons_pressed[Button.RIGHT_PLUS] == 20:
        #     self.up_button_pressed(Port.B)
        #     self._buttons_pressed[Button.RIGHT_PLUS] = 0
        # elif self._buttons_pressed[Button.RIGHT_MINUS] == 20:
        #     self.down_button_pressed(Port.B)
        #     self._buttons_pressed[Button.RIGHT_MINUS] = 0

class TrainMotor(object):
    def __init__(self, port, id):
        if id == 1 or id == 2:  #dumb motor
            self._motor = DCMotor(port) 
        elif id == 46 or id == 47:  #smart motor
            self._motor = Motor(port)
        self._power = 0
        # self._power_increment = 10
        self._spinning = 0 # 1 left 2 right
        self._straight = 0 # 1 forward 2 backward

    # def start_spinning(self, direction):
    #     if direction != self._spinning:
    #         if direction == 1:
    #             self._motor.dc(100)
    #         else:
    #             self._motor.dc(-100)
    #         self._spinning = direction

    # def go_straight(self, direction)
    #     if direction != self._spinning:
    #         if direction == 1:
    #             self._motor.dc(100)
    #         else:
    #             self._motor.dc(-100)
    #         self._spinning = direction

    def get_power(self):
        return self._power

    def set_power(self, power):
        if self._power != power:
            self._motor.dc(power)
        self._power = power

    # def decrease_power(self):
    #     self._power -= self._power_increment
    #     if self._power < -100:
    #         self._power = -100
    #     self._motor.dc(self._power)

    # def increase_power(self):
    #     self._power += self._power_increment
    #     if self._power > 100:
    #         self._power = 100
    #     self._motor.dc(self._power)

    def stop(self):
        self._power = 0
        self._motor.stop()

train_hub = TrainHub()

while True:
    train_hub.run()

    # Wait so we can see the result.
    #wait(10)
