from pybricks.tools import StopWatch, wait
from pybricks.hubs import TechnicHub
import HubConfig
from pybricks.parameters import Port
from pybricks.pupdevices import ColorDistanceSensor
import Colours
import Constants

_BROADCAST_INTERVAL = 5000
_DETECT_DISTANCE = 80


def wait_for_colour(sensor):
    while True:
        colour = Colours.get_colour(sensor)

        if colour != Colours.NONE:
            print(colour)
            return colour

        wait(100)


def get_config():
    sensor = ColorDistanceSensor(Port.D)
    colour_code = wait_for_colour(sensor)
    return HubConfig.get_controller_config(colour_code)


class ControllerHub:
    is_broadcasting = False
    sensor_off = False

    def __init__(self):
        self.hub_config = get_config()

        self.hub = TechnicHub(
            broadcast_channel=self.hub_config[HubConfig.HC_B_CHAN],
            observe_channels=self.hub_config[HubConfig.HC_O_CHANS],
        )
        self.hub.light.on(self.hub_config[HubConfig.HC_COLOUR])

        self.broadcast_timer = StopWatch()
        self.sensor = ColorDistanceSensor(Port.D)

    def broadcast(self, message) -> None:
        self.is_broadcasting = True
        self.broadcast_timer.reset()
        self.broadcast_timer.resume()
        self.hub.ble.broadcast(message)

    def check_broadcast(self) -> None:
        if not self.is_broadcasting:
            return

        if self.broadcast_timer.time() < _BROADCAST_INTERVAL:
            return

        self.stop_broadcasting()

    def stop_broadcasting(self) -> None:
        self.is_broadcasting = False
        self.hub.ble.broadcast(Constants.Msg_Ping)
        self.broadcast_timer.pause()

    def observe(self):
        self.check_broadcast()

        messages = []
        for channel in self.hub_config[HubConfig.HC_O_CHANS]:
            received = self.hub.ble.observe(channel)

            if received is not None:
                messages.append(received)

        return list(messages)

    def turn_sensor_off(self) -> None:
        if self.sensor_off:
            return

        self.sensor.light.off()
        self.sensor_off = True

    def is_sensor_triggered(self) -> bool:
        self.sensor_off = False
        distance = self.sensor.distance()

        if distance < _DETECT_DISTANCE:
            self.turn_sensor_off()
            return True

        return False
