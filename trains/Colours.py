GREY = 1
BLUE = 2
RED = 3
YELLOW = 4
TEAL = 5
GREEN = 6
NONE = 7
MEDIUMBLUE = 8


def get_colour(sensor):
    color = sensor.hsv()
    if (
        color.v > 55
        and color.h > 200
        and color.h < 230
        and color.s > 30
        and color.s < 40
    ):
        return GREY
    elif color.v > 55 and color.h > 210 and color.h < 230 and color.s > 90:
        return BLUE
    elif color.v > 50 and color.h > 207 and color.h < 226 and color.s > 65:
        return MEDIUMBLUE
    elif color.v > 55 and color.h > 350 and color.h < 360 and color.s > 90:
        return RED
    elif color.v > 55 and color.h > 50 and color.h < 60 and color.s > 85:
        return YELLOW
    elif color.v > 30 and color.h > 170 and color.h < 215 and color.s > 65:
        return TEAL
    elif color.v > 65 and color.h > 85 and color.h < 92 and color.s > 70:
        return "limegreen"
    elif color.v > 43 and color.h > 120 and color.h < 140:
        return GREEN

    return NONE


SC_KM = BLUE
SC_HIToKM = YELLOW
SC_HIToBN = RED
SC_BN = GREEN
