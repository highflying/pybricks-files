from pybricks.tools import wait
from pybricks.parameters import Color
import Colours
import Batches


def wait_for_colour(sensor):
    while True:
        colour = Colours.get_colour(sensor)

        if colour != Colours.NONE:
            print(colour)
            return colour

        wait(100)


def get_init_batch(train):
    colour_code = wait_for_colour(train.sensor)
    if colour_code == Colours.SC_KM:
        train.light(Color.BLUE)
        return Batches.get_batch(Batches.KMSTART)
    elif colour_code == Colours.SC_BN:
        train.light(Color.GREEN)
        return Batches.get_batch(Batches.BNSTART)
    elif colour_code == Colours.SC_HIToBN:
        train.light(Color.RED)
        return Batches.get_batch(Batches.HITOBNSTART)

    train.light(Color.YELLOW)
    return Batches.get_batch(Batches.HITOKMSTART)
