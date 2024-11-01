from pybricks.hubs import CityHub
from HubConfig import get_hub_config
from pybricks.parameters import Color
from Messages import Messages
from Colours import ColourSensor
from TrainMotor import TrainMotor
from pybricks.tools import wait
from TrainType import TrainType


class TrainHub:
    current_power = 0

    def __init__(self):
        hub = CityHub()

        self.hub_config = get_hub_config(hub.system.name())

        self.hub = CityHub(
            broadcast_channel=self.hub_config.broadcast_channel,
            observe_channels=[self.hub_config.observe_channel],
        )

        self.motor = TrainMotor(self.hub_config.slow_power, self.hub_config.fast_power)
        self.sensor = ColourSensor()

        self.light(Color.GREEN)
        self.broadcast(Messages.Stopped)

    def stop(self):
        self.motor.stop()
        self.broadcast(Messages.Stopped)

    def stop_and_reverse(self):
        self.motor.stop()
        wait(1000)
        self.motor.reverse()
        self.broadcast(Messages.Running)

    def reverse(self):
        self.motor.reverse()
        self.broadcast(Messages.Running)

    def slow(self):
        self.motor.slow()
        self.broadcast(Messages.Running)

    def fast(self):
        self.motor.fast()
        self.broadcast(Messages.Running)

    def light(self, color):
        self.hub.light.on(color)

    def broadcast(self, message):
        self.hub.ble.broadcast(message)

    def observe(self):
        return self.hub.ble.observe(self.hub_config.observe_channel)

    def is_passenger(self):
        return self.hub_config.train_type == TrainType.Passenger

    def is_goods(self):
        return self.hub_config.train_type == TrainType.Goods

    def is_stopped(self):
        return self.motor.is_stopped()

    def is_reversing(self):
        return self.motor.is_reversing()

    def is_slow(self):
        return self.motor.is_slow()

    def get_colour(self):
        return self.sensor.get_colour()
