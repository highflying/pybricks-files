from pybricks.pupdevices import ColorDistanceSensor
from pybricks.parameters import Port


class HSVColorClass:
    GREY = "grey"
    BLUE = "blue"
    RED = "red"
    YELLOW = "yellow"
    TEAL = "teal"
    GREEN = "green"
    NONE = "none"
    MEDIUMBLUE = "mediumblue"


HSVColor = HSVColorClass()


def get_colour(sensor):
    color = sensor.hsv()
    if (
        color.v > 55
        and color.h > 200
        and color.h < 230
        and color.s > 30
        and color.s < 40
    ):
        return HSVColor.GREY
    elif color.v > 55 and color.h > 210 and color.h < 230 and color.s > 90:
        return HSVColor.BLUE
    elif color.v > 50 and color.h > 207 and color.h < 226 and color.s > 75:
        return HSVColor.MEDIUMBLUE
    elif color.v > 55 and color.h > 350 and color.h < 360 and color.s > 90:
        return HSVColor.RED
    elif color.v > 55 and color.h > 50 and color.h < 60 and color.s > 85:
        return HSVColor.YELLOW
    elif color.v > 30 and color.h > 170 and color.h < 202 and color.s > 85:
        return HSVColor.TEAL
    elif color.v > 65 and color.h > 85 and color.h < 92 and color.s > 70:
        return "limegreen"
    elif color.v > 43 and color.h > 120 and color.h < 140:
        return HSVColor.GREEN

    return HSVColor.NONE


class ColourSensor:
    def __init__(self, port=Port.B):
        self.sensor = ColorDistanceSensor(port)

    def get_colour(self):
        return get_colour(self.sensor)
