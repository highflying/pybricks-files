from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, Light, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = CityHub()

motor = DCMotor(Port.A)
sensor = ColorDistanceSensor(Port.B)

power = 50;
# print(sensor.detectable_colors());
# hub.light.on(Color.YELLOW);
# motor.dc(power)

def get_color():
    color = sensor.hsv();
    if color.v > 40:
        print(color);
        if color.h > 200 and color.h < 230 and color.s > 30 and color.s< 40:
            return 'grey';
        elif color.h > 210 and color.h < 230 and color.s > 90:
            return 'blue';
        elif color.h > 350 and color.h < 360:
            return 'red';
        elif color.h > 50 and color.h < 60:
            return 'yellow';
        elif color.h > 180 and color.h < 190:
            return 'teal';
        elif color.h > 130 and color.h < 140:
            return 'green';
    return 'none'

prev_color='none'
while True:
    got_color = get_color();

    if got_color != 'none' and prev_color != got_color:
        print(got_color);
        prev_color = got_color;

    # if prev_color != got_color and got_color != Color.NONE: # and got_color != Color.BLUE and got_color != Color.GREEN:
    #     hub.light.on(got_color)
    #     print(got_color)
    #     prev_color = got_color
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
    
