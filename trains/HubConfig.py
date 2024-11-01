from Channels import Channels
from TrainType import TrainType


class HubConfig:
    name = "Hub Name"
    broadcast_channel = 0
    observe_channel = 0
    train_type = TrainType.Passenger
    fast_power = 0
    slow_power = 0


class OuterLoopController(HubConfig):
    name = "Outer Loop Controller"
    broadcast_channel = Channels.OuterLoopController
    observe_channel = Channels.OuterLoopTrain


class InnerLoopController(HubConfig):
    name = "Controller Hub"
    broadcast_channel = Channels.InnerLoopController
    observe_channel = Channels.InnerLoopTrain


class Autocoach(HubConfig):
    name = "Autocoach Hub"
    broadcast_channel = Channels.InnerLoopTrain
    observe_channel = Channels.InnerLoopController
    fast_power = -80
    slow_power = -55


class Tram(HubConfig):
    name = "Goods Train Hub"
    broadcast_channel = Channels.InnerLoopTrain
    observe_channel = Channels.InnerLoopController
    train_type = TrainType.Goods
    fast_power = -60
    slow_power = -58


class WhiteCoach(HubConfig):
    name = "White Coach Hub"
    broadcast_channel = Channels.OuterLoopTrain
    observe_channel = Channels.OuterLoopController
    fast_power = 100
    slow_power = 100


def get_hub_config(name: str):
    if name == OuterLoopController.name:
        return OuterLoopController
    elif name == InnerLoopController.name:
        return InnerLoopController
    elif name == Autocoach.name:
        return Autocoach
    elif name == Tram.name:
        return Tram
    elif name == WhiteCoach.name:
        return WhiteCoach

    raise Exception("Hub not found")
