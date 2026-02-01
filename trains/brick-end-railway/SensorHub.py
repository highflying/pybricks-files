from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, ColorDistanceSensor, Light
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = TechnicHub()

sensor = ColorDistanceSensor(Port.A)
light = Light(Port.B)
count = 0

while True:
    distance = sensor.distance()

    if distance <= 70:
        count = count + 1

        if count > 10:
            light.on()
            wait(1000)
            light.off()
            count = 0
        else:
            wait(300)
    else:
        wait(100)



    # print(distance, count)
    # wait(100)