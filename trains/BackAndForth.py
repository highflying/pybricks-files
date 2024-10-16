from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, Light, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = CityHub()

motor = DCMotor(Port.A)
sensor = ColorDistanceSensor(Port.B)

power = 40

hub.light.on(Color.YELLOW)

while True:
    got_color = sensor.color()

    if got_color == Color.RED:
        # print('red');
        motor.brake()
        wait(5000)
        power = power * -1
        motor.dc(power)
        wait(1000)

    # elif got_color == Color.BLUE:
    #     print('blue')
    #     motor.stop();
    #     wait(5000);
    #     motor.dc(power);
    #     wait(1000);

    # elif got_color == Color.GREEN:
    #     print('green')
    #     motor.stop();

    else:
        wait(20)

    volts = hub.battery.voltage()
    print(volts)

    if volts < 5000:
        hub.light.blink(Color.YELLOW, [500, 500])
