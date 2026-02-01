from pybricks.tools import wait
from LightHub import LightHub

light = LightHub('ghostcont')

while True:
    light.controller()

    wait(100)
