import Constants
import Colours
from pybricks.parameters import Color

HC_NAME = 0
HC_B_CHAN = 1
HC_O_CHANS = 2
HC_FAST = 3
HC_SLOW = 4
HC_REMOTE = 5
HC_COLOUR = 6


def get_controller_config(color):
    if color == Colours.YELLOW:
        return [
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
    elif color == Colours.RED:
        return [
            Constants.Channel_OuterCont,
            [Constants.Channel_OuterTrain],
            0,
            0,
            None,
            Color.GREEN,
        ]

    return [
        "Controller Hub",
        Constants.Channel_InnerCont,
        [Constants.Channel_InnerTrain],
        0,
        0,
        None,
        Color.GREEN,
    ]


def get_hub_config(name: str):
    if name == "Autocoach Hub":
        return [
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
    elif name == "Goods Train Hub":
        return [
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
    elif name == "White Coach Hub":
        return [
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

    raise Exception("Hub not found")
