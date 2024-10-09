from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, Light, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = CityHub()

motor = DCMotor(Port.A)
sensor = ColorDistanceSensor(Port.B)

power = 50;

hub.light.on(Color.YELLOW);
# motor.dc(power)
prev_color=Color.NONE
while True:
    got_color = sensor.color();

    
    if prev_color != got_color and got_color != Color.NONE: # and got_color != Color.BLUE and got_color != Color.GREEN:
        hub.light.on(got_color)
        print(got_color)
        prev_color = got_color
    # if got_color == Color.RED:
    #     print('red');
    #     hub.light.on(Color.RED)
    #     motor.brake();
    #     wait(5000);
    #     power = power * -1;
    #     motor.dc(power);
    #     wait(1000);

    # elif got_color == Color.BLUE:
    #     print('blue')
    #     motor.stop();
    #     wait(5000);
    #     motor.dc(power);
    #     wait(1000);

    # elif got_color == Color.GREEN:
    #     print('green')
    #     motor.stop();

    # else:
    wait(20);

    # volts = hub.battery.voltage();
    # print(volts)

    # if volts < 5000:
    #     hub.light.blink(Color.YELLOW, [500, 500])
    
