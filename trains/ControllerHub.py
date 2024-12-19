from pybricks.tools import StopWatch, wait
from pybricks.hubs import TechnicHub
import HubConfig
from pybricks.parameters import Color, Port
from pybricks.pupdevices import ColorDistanceSensor
from DistanceSensor import DistanceSensor
import Colours
import Constants

BROADCAST_INTERVAL = 5000


def wait_for_colour(sensor):
    while True:
        colour = Colours.get_colour(sensor)

        if colour != Colours.NONE:
            print(colour)
            return colour

        wait(500)


def get_config():
    sensor = ColorDistanceSensor(Port.D)
    colour_code = wait_for_colour(sensor)
    if colour_code == Colours.YELLOW:
        print("hi")
        return HubConfig.HIController
    elif colour_code == Colours.RED:
        print("out")
        return HubConfig.OuterLoopController

    print("in")
    return HubConfig.InnerLoopController


class ControllerHub:
    is_broadcasting = False
    previous_received = None

    def __init__(self):
        self.hub_config = get_config()

        self.hub = TechnicHub(
            broadcast_channel=self.hub_config[HubConfig.HC_B_CHAN],
            observe_channels=self.hub_config[HubConfig.HC_O_CHANS],
        )
        self.hub.light.on(self.hub_config[HubConfig.HC_COLOUR])

        self.broadcast_timer = StopWatch()
        self.sensor = DistanceSensor()

    def broadcast(self, message) -> None:
        self.is_broadcasting = True
        self.broadcast_timer.reset()
        self.broadcast_timer.resume()
        self.hub.ble.broadcast(message)

    def check_broadcast(self) -> None:
        if not self.is_broadcasting:
            return

        if self.broadcast_timer.time() < BROADCAST_INTERVAL:
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

    def sensor_off(self) -> None:
        self.sensor.off()

    def is_sensor_triggered(self) -> bool:
        return self.sensor.is_triggered()