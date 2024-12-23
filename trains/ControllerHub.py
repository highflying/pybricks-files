from pybricks.tools import StopWatch
from pybricks.hubs import TechnicHub
from HubConfig import get_hub_config
from pybricks.parameters import Color
from DistanceSensor import DistanceSensor
from Messages import Messages

BROADCAST_INTERVAL = 5000


class ControllerHub:
    is_broadcasting = False
    previous_received = None

    def __init__(self):
        hub = TechnicHub()

        self.hub_config = get_hub_config(hub.system.name())

        self.hub = TechnicHub(
            broadcast_channel=self.hub_config.broadcast_channel,
            observe_channels=[self.hub_config.observe_channel],
        )

        self.broadcast_timer = StopWatch()
        self.sensor = DistanceSensor()

    def broadcast(self, message) -> None:
        self.is_broadcasting = True
        self.broadcast_timer.reset()
        self.broadcast_timer.resume()
        self.hub.ble.broadcast(message)
        self.hub.light.on(Color.YELLOW)

    def check_broadcast(self) -> None:
        if not self.is_broadcasting:
            return

        if self.broadcast_timer.time() < BROADCAST_INTERVAL:
            return

        self.stop_broadcasting()

    def stop_broadcasting(self) -> None:
        self.is_broadcasting = False
        self.hub.ble.broadcast(Messages.Ping)  # type: ignore
        self.broadcast_timer.pause()
        self.hub.light.on(Color.GREEN)

    def observe(self):
        self.check_broadcast()

        received = self.hub.ble.observe(self.hub_config.observe_channel)

        if received is not None and self.previous_received != received:
            self.previous_received = received
            return received

        return None

    def light(self, color: Color) -> None:
        self.hub.light.on(color)

    def sensor_off(self) -> None:
        self.sensor.off()

    def is_sensor_triggered(self) -> bool:
        return self.sensor.is_triggered()
