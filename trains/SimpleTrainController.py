from pybricks.hubs import CityHub
from pybricks.pupdevices import Remote, DCMotor, ColorDistanceSensor
from pybricks.parameters import Button, Port
from pybricks.tools import wait

hub = CityHub()
remote = Remote(timeout=30000)

motor = DCMotor(Port.A)
power = 0

try:
    sensor = ColorDistanceSensor(Port.B)
    sensor.light.off()
except:
    print("Sensor not found")

while True:
    pressed = remote.buttons.pressed()

    if Button.LEFT_PLUS in pressed:
        if power < 100:
            power = power + 10
            motor.dc(power)
            wait(500)

    elif Button.LEFT_MINUS in pressed:
        if power > -100:
            power = power - 10
            motor.dc(power)
            wait(500)

    elif Button.LEFT in pressed:
        power = 0
        motor.stop()

    wait(10)
