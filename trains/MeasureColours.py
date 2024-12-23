from pybricks.hubs import CityHub
from pybricks.pupdevices import ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait
from Colours import get_colour

hub = CityHub()

sensor = ColorDistanceSensor(Port.B)

hub.light.on(Color.YELLOW)

while True:
    got_color = sensor.hsv()

    colourName = get_colour(sensor)

    if colourName != "none":
        print(got_color)
        print(colourName)

    wait(500)
