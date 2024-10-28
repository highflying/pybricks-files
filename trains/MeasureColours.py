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

    colourName = get_colour(sensor);
    print(got_color);

    if colourName == 'teal' or colourName == 'mediumblue':
        print(got_color);
        print(colourName)

    wait(500);