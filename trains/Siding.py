from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, Light, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from Colours import HSVColor, get_colour
from Power import ramp_power

hub = CityHub()
hub.light.on(Color.NONE)

motor = DCMotor(Port.A)
sensor = ColorDistanceSensor(Port.B)

fast_power = 50
slow_power = 40
use_siding = True

ramp_power(motor, 0, fast_power)

prev_color = HSVColor.NONE
in_siding = False

while True:
    got_color = get_colour(sensor)

    if prev_color == got_color or got_color == HSVColor.NONE:
        continue

    prev_color = got_color

    print(got_color, in_siding)

    if got_color == HSVColor.RED:
        if use_siding and not in_siding:
            print("skip")
        else:
            # stop, wait and go forward
            hub.light.on(Color.RED)
            motor.stop()
            wait(5000)
            ramp_power(motor, 0, fast_power, 100)
            wait(1000)

    elif got_color == HSVColor.BLUE:
        # slow down
        hub.light.on(Color.BLUE)
        ramp_power(motor, fast_power, slow_power, 50)
        wait(1000)

    elif got_color == HSVColor.TEAL:
        if not use_siding:
            continue

        if in_siding == True:
            in_siding = False
            wait(1000)

        else:
            # stop, wait, reverse
            hub.light.on(Color.CYAN)
            motor.stop()
            wait(1000)
            ramp_power(motor, 0, slow_power * -1)
            wait(1000)
            in_siding = True

    else:
        wait(10)
