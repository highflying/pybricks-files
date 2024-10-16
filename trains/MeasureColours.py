from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, Light, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, run_task
from Colours import HSVColor, get_colour

hub = CityHub()

sensor = ColorDistanceSensor(Port.B)

hub.light.on(Color.YELLOW);

while True:
    got_color = sensor.hsv();

    print(got_color);

    colourName = get_colour(sensor);

    print(colourName)

    wait(500);