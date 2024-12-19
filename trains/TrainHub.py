import HubConfig
from pybricks.hubs import CityHub
from pybricks.parameters import Button, Port
from pybricks.pupdevices import Remote, DCMotor, ColorDistanceSensor
from pybricks.tools import StopWatch
import Constants
from Colours import get_colour

_MIN_BUTTON_INTERVAL = 1000


class TrainHub:
    current_power = 0
    direction = 1

    def __init__(self):
        hub = CityHub()

        self.hub_config = HubConfig.get_hub_config(hub.system.name())

        self.hub = CityHub(
            broadcast_channel=self.hub_config[HubConfig.HC_B_CHAN],
            observe_channels=self.hub_config[HubConfig.HC_O_CHANS],
        )

        if self.hub_config[HubConfig.HC_REMOTE] is not None:
            print("Looking for remote", self.hub_config[HubConfig.HC_REMOTE])
            self.remote = Remote(
                name=self.hub_config[HubConfig.HC_REMOTE], timeout=30000
            )
            self.remote.light.on(self.hub_config[HubConfig.HC_COLOUR])
            self.button_timer = StopWatch()

        self.motor = DCMotor(Port.A)
        self.sensor = ColorDistanceSensor(Port.B)
        self.direction = 1

        self.light(self.hub_config[HubConfig.HC_COLOUR])

    def perform_regular_checks(self):
        if self.button_timer.time() > _MIN_BUTTON_INTERVAL:
            pressed = self.remote.buttons.pressed()

            if Button.LEFT_PLUS in pressed:
                self.fast()
                self.button_timer.reset()

            elif Button.LEFT_MINUS in pressed:
                self.slow()
                self.button_timer.reset()

            elif Button.LEFT in pressed:
                self.stop()
                self.button_timer.reset()

    def stop(self):
        self.current_power = 0
        self.motor.stop()

    def toggle_direction(self):
        self.direction *= -1

    def slow(self):
        self.current_power = self.hub_config[HubConfig.HC_SLOW] * self.direction
        self.motor.dc(self.current_power)

    def fast(self):
        self.current_power = self.hub_config[HubConfig.HC_FAST] * self.direction
        self.motor.dc(self.current_power)

    def light(self, color):
        self.hub.light.on(color)

    def broadcast(self, message):
        # print('broadcast', self.hub_config.broadcast_channel, message)
        self.hub.ble.broadcast(message)

    def observe(self):
        messages = []
        for channel in self.hub_config[HubConfig.HC_O_CHANS]:
            received = self.hub.ble.observe(channel)

            if received is not None and received != Constants.Msg_Ping:
                messages.append(received)

        return list(messages)

    def is_stopped(self):
        return self.current_power == 0

    def is_reversing(self):
        return self.current_power == self.hub_config[HubConfig.HC_SLOW] * -1

    def is_slow(self):
        return self.current_power == self.hub_config[HubConfig.HC_SLOW]

    def get_colour(self):
        return get_colour(self.sensor)
