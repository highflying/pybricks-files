import HubConfig
from pybricks.parameters import Button, Port, Color
from pybricks.pupdevices import Remote, DCMotor, ColorDistanceSensor
from pybricks.iodevices import PUPDevice
from pybricks.tools import StopWatch, wait
from uerrno import ENODEV
import Constants
import Colours
import Batches

_MIN_BUTTON_INTERVAL = 1000
_DETECT_DISTANCE = 80


def get_device_id(port):
    try:
        device = PUPDevice(port)
        return device.info()["id"]
    except OSError as ex:
        if ex.args[0] == ENODEV:
            return 0
        else:
            raise


def wait_for_colour(sensor):
    while True:
        colour = Colours.get_colour(sensor)

        if colour != Colours.NONE:
            print(colour)
            return colour

        wait(100)


def get_devices():
    ports = [Port.A, Port.B]

    # On hubs that support it, add more ports.
    try:
        ports.append(Port.C)
        ports.append(Port.D)
    except AttributeError:
        pass

    sensors = []
    motors = []

    for port in ports:
        found_device = get_device_id(port)
        if found_device == 2:
            motors.append(DCMotor(port))
        elif found_device == 37:
            sensors.append(ColorDistanceSensor(port))

    return sensors, motors


def get_init_batch(train):
    colour_code = wait_for_colour(train.sensor)
    if colour_code == Colours.SC_KM:
        train.light(Color.BLUE)
        return Batches.get_batch(Batches.KMSTART)
    elif colour_code == Colours.SC_BN:
        train.light(Color.GREEN)
        return Batches.get_batch(Batches.BNSTART)
    elif colour_code == Colours.SC_HIToBN:
        train.light(Color.RED)
        return Batches.get_batch(Batches.HITOBNSTART)

    train.light(Color.YELLOW)
    return Batches.get_batch(Batches.HITOKMSTART)


class TrainHub:
    current_power = 0
    direction = 1
    remote = None
    button_timer = None

    def __init__(self):
        try:
            from pybricks.hubs import CityHub

            hubFunc = CityHub
        except:
            pass

        try:
            from pybricks.hubs import TechnicHub

            hubFunc = TechnicHub
        except:
            pass

        hub = hubFunc()

        hubName = hub.system.name()

        sensors, motors = get_devices()

        if hubName == "controller":
            colour_code = wait_for_colour(sensors[0])
            self.hub_config = HubConfig.get_hub_config_by_colour(colour_code)
        else:
            self.hub_config = HubConfig.get_hub_config_by_name(hubName)

        self.hub = hubFunc(
            broadcast_channel=self.hub_config[Constants.HC_BroadcastChannel],
            observe_channels=self.hub_config[Constants.HC_ObserveChannels],
        )

        if self.hub_config[Constants.HC_RemoteName] is not None:
            print("Looking for remote", self.hub_config[Constants.HC_RemoteName])
            self.remote = Remote(
                name=self.hub_config[Constants.HC_RemoteName], timeout=30000
            )
            self.remote.light.on(self.hub_config[Constants.HC_Colour])
            self.button_timer = StopWatch()

        if len(motors) > 0:
            self.motor = motors[0]
        if len(sensors) > 0:
            self.sensor = sensors[0]

        self.direction = 1
        self.broadcast(Constants.Msg_Ping)

        self.light(self.hub_config[Constants.HC_Colour])

    def get_initial_batch(self):
        if self.hub.system.name() == "controller":
            if self.hub_config[Constants.HC_InitialBatch] is not None:
                return Batches.get_batch(self.hub_config[Constants.HC_InitialBatch])
            else:
                return []
        else:
            return get_init_batch(self)

    def perform_regular_checks(self):
        if (
            self.remote is not None
            and self.button_timer is not None
            and self.button_timer.time() > _MIN_BUTTON_INTERVAL
        ):
            pressed = self.remote.buttons.pressed()

            if Button.LEFT_PLUS in pressed:
                self.hub_config[Constants.HC_FastPower] += 5
                if self.hub_config[Constants.HC_FastPower] > 100:
                    self.hub_config[Constants.HC_FastPower] = 100
                self.button_timer.reset()
            elif Button.LEFT_MINUS in pressed:
                self.hub_config[Constants.HC_FastPower] -= 5
                if self.hub_config[Constants.HC_FastPower] < 20:
                    self.hub_config[Constants.HC_FastPower] = 20
                self.button_timer.reset()
            elif Button.LEFT in pressed:
                self.stop()
                self.button_timer.reset()
            if Button.RIGHT_PLUS in pressed:
                self.hub_config[Constants.HC_SlowPower] += 5
                if self.hub_config[Constants.HC_SlowPower] > 100:
                    self.hub_config[Constants.HC_SlowPower] = 100
                self.button_timer.reset()
            elif Button.RIGHT_MINUS in pressed:
                self.hub_config[Constants.HC_SlowPower] -= 5
                if self.hub_config[Constants.HC_SlowPower] < 20:
                    self.hub_config[Constants.HC_SlowPower] = 20
                self.button_timer.reset()
            elif Button.RIGHT in pressed:
                self.button_timer.reset()
                return True

        return False

    def stop(self):
        self.current_power = 0
        if self.motor:
            self.motor.stop()

    def move_forward(self):
        self.direction = 1

    def move_backwards(self):
        self.direction = -1

    def slow(self):
        self.current_power = self.hub_config[Constants.HC_SlowPower] * self.direction
        if self.motor:
            self.motor.dc(self.current_power)

    def fast(self):
        self.current_power = self.hub_config[Constants.HC_FastPower] * self.direction
        if self.motor:
            self.motor.dc(self.current_power)

    def light(self, color):
        self.hub.light.on(color)

    def broadcast(self, message):
        print("broadcast", self.hub_config[Constants.HC_BroadcastChannel], message)
        self.hub.ble.broadcast(message)
        wait(2000)
        self.hub.ble.broadcast(None)

    def observe(self):
        messages = []
        for channel in self.hub_config[Constants.HC_ObserveChannels]:
            received = self.hub.ble.observe(channel)
            # print('channel', channel)
            if received is not None and received != Constants.Msg_Ping:
                # print('received', received)
                messages.append(received)

        return list(messages)

    def is_stopped(self):
        return self.current_power == 0

    def is_reversing(self):
        return self.current_power == self.hub_config[Constants.HC_SlowPower] * -1

    def is_slow(self):
        return self.current_power == self.hub_config[Constants.HC_SlowPower]

    def get_colour(self):
        if self.sensor:
            return Colours.get_colour(self.sensor)

        return Colours.NONE

    def turn_sensor_off(self) -> None:
        if self.sensor_off:
            return

        if self.sensor:
            self.sensor.light.off()
        self.sensor.light.off()
        self.sensor_off = True

    def is_sensor_triggered(self) -> bool:
        self.sensor_off = False

        if not self.sensor:
            return False

        distance = self.sensor.distance()

        if distance < _DETECT_DISTANCE:
            self.turn_sensor_off()
            return True

        return False
