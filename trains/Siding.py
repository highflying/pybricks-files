from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, Light, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = CityHub()

motor = DCMotor(Port.A)
sensor = ColorDistanceSensor(Port.B)

def get_color():
    color = sensor.hsv();
    if color.v > 60:
        # print(color);
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

    return 'none';


fast_power = 50;
slow_power = 40;

hub.light.on(Color.NONE);

in_siding = False;

def ramppower(fromPower, toPower, ms = 250):
    p = fromPower;
    mult = 2;
    if fromPower > toPower:
        mult = -2;
    print('start ramp', fromPower, toPower, ms)
    while (fromPower > toPower and p > toPower) or (fromPower < toPower and p < toPower):
        p = p + mult;
        motor.dc(p);
        wait(ms);
    print('end ramp');
    
    return;

ramppower(0, fast_power);
use_siding = True

prev_color = 'none';

while True:
    got_color = get_color();

    if prev_color == got_color or got_color == 'none': 
        continue;

    prev_color = got_color;

    print(got_color, in_siding);

    if got_color == 'red':
        if use_siding and not in_siding:
            print('skip')
        else:
            hub.light.on(Color.RED);
            motor.stop();
            wait(5000);
            ramppower(0, fast_power, 100);
            wait(1000);

    elif got_color == 'yellow':
        hub.light.on(Color.YELLOW);
        ramppower(fast_power, slow_power, 50)
        wait(1000);
    elif got_color == 'teal':
        if not use_siding:
            continue;

        if in_siding == True:
            in_siding = False;
            wait(1000);

        else:
            hub.light.on(Color.WHITE);
            motor.stop();
            wait(1000);
            ramppower(0, slow_power * -1);
            wait(1000);
            in_siding = True;


    # elif got_color == 'teal':
    #     hub.light.blink(Color.CYAN,[500,500]);
    # elif got_color == 'blue':
    #     hub.light.blink(Color.BLUE,[500,500]);

    #     print('blue')
    #     motor.stop();
    #     wait(5000);
    #     motor.dc(power);
    #     wait(1000);

    # elif got_color == Color.GREEN:
    #     print('green')
    #     motor.stop();

    else:
        wait(10);

    # volts = hub.battery.voltage();
    # print(volts)

    # if volts < 5000:
    #     hub.light.blink(Color.YELLOW, [500, 500])
    
# def slow_down(from, to):
#     p = from;

#     while p > to:
#         p = p - 2;
#         motor.dc(p);
#         wait(250);

# def speed_up(from, to):
#     p = from;

#     while p < to:
#         p = p + 2;
#         motor.dc(p);
#         wait(250);

# def ramp_power(from, to):
#     p = from;
#     mult = 2;
#     if from > to:
#         mult = -2;
    
#     while (from > to and p > to) or (from < to and p < to):
#         p = p + mult;
#         motor.dc(p);
#         wait(250);
    