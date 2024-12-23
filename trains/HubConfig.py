import Constants
from pybricks.parameters import Color

HC_NAME = 0
HC_B_CHAN = 1
HC_O_CHANS = 2
HC_FAST = 3
HC_SLOW = 4
HC_REMOTE = 5
HC_COLOUR = 6

HIController = [
    "Controller Hub",
    Constants.Channel_HIController,
    [
        Constants.Channel_RedTrain,
        Constants.Channel_BlueTrain,
        Constants.Channel_GreenTrain,
    ],
    0,
    0,
    None,
    Color.YELLOW,
]

OuterLoopController = [
    "Outer Loop Cont",
    Constants.Channel_OuterCont,
    [Constants.Channel_OuterTrain],
    0,
    0,
    None,
    Color.GREEN,
]

InnerLoopController = [
    "Controller Hub",
    Constants.Channel_InnerCont,
    [Constants.Channel_InnerTrain],
    0,
    0,
    None,
    Color.GREEN,
]


Autocoach = [
    "Autocoach Hub",
    Constants.Channel_BlueTrain,
    [
        Constants.Channel_RedTrain,
        Constants.Channel_GreenTrain,
        Constants.Channel_HIController,
    ],
    -60,
    -40,
    "blue",
    Color.BLUE,
]

Tram = [
    "Goods Train Hub",
    Constants.Channel_RedTrain,
    [
        Constants.Channel_BlueTrain,
        Constants.Channel_GreenTrain,
        Constants.Channel_HIController,
    ],
    -55,
    -50,
    "red",
    Color.RED,
]


WhiteCoach = [
    "White Coach Hub",
    Constants.Channel_GreenTrain,
    [
        Constants.Channel_BlueTrain,
        Constants.Channel_RedTrain,
        Constants.Channel_HIController,
    ],
    85,
    50,
    "green",
    Color.GREEN,
]


def get_hub_config(name: str):
    if name == Autocoach[HC_NAME]:
        return Autocoach
    elif name == Tram[HC_NAME]:
        return Tram
    elif name == WhiteCoach[HC_NAME]:
        return WhiteCoach

    raise Exception("Hub not found")
