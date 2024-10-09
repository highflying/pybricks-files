from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, Light, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = CityHub()

motor = DCMotor(Port.A)
sensor = ColorDistanceSensor(Port.B)

fast_power = 60;
slow_power = 40;

hub.light.on(Color.NONE);
motor.dc(fast_power);

while True:
    got_color = sensor.color();

    if got_color == Color.RED:
        hub.light.on(got_color);
        print(got_color);
        motor.brake();
        wait(5000);
        # power = power * -1;
        motor.dc(fast_power);
        # wait(1000);
    elif got_color == Color.YELLOW:
        hub.light.on(got_color);
        print(got_color)
        motor.dc(slow_power)
        wait(1000);

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
        wait(20);

    # volts = hub.battery.voltage();
    # print(volts)

    # if volts < 5000:
    #     hub.light.blink(Color.YELLOW, [500, 500])
    
