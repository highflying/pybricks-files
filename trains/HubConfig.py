import Constants
import Colours
from pybricks.parameters import Color
import Batches


def get_hub_config_by_colour(colour):
    if colour == Colours.YELLOW:
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
            Batches.HIGHLEY_CONTROLLER,
        ]
    elif colour == Colours.RED:
        return [
            Constants.Channel_OuterCont,
            [Constants.Channel_OuterTrain],
            0,
            0,
            None,
            Color.GREEN,
            Batches.OUTER_CONTROLLER,
        ]

    return [
        Constants.Channel_InnerCont,
        [Constants.Channel_InnerTrain],
        0,
        0,
        None,
        Color.GREEN,
        Batches.INNER_CONTROLLER,
    ]


def get_hub_config_by_name(name: str):
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
