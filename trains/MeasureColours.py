from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, Light, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, run_task
from Colours import HSVColor, get_colour

hub = CityHub()

sensor = ColorDistanceSensor(Port.B)

hub.light.on(Color.YELLOW);


async def main():
    while True:
        got_color = await sensor.hsv();

        print(got_color);

        colourName = await get_colour(sensor);

        print(colourName)

        await wait(500);

run_task(main())