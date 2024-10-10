from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait, multitask, run_task, StopWatch
from Colours import HSVColor, get_colour
from Power import ramp_power

hub = CityHub(broadcast_channel=2,observe_channels=[1]);

motor = DCMotor(Port.A);
sensor = ColorDistanceSensor(Port.B);

fast_power = 50;
slow_power = 40;

hub.light.on(Color.RED);

current_power = 0;
broadcast_msg = 'stopped';

Event_Stop_Train = const('stop_train');
Event_Start_Train = const('start_train');
Event_Slow_Train = const('slow_train');

events = [];

async def handle_broadcast():
    global broadcast_msg;
    prev_broadcast_msg = None;
    timer = StopWatch();

    while True:
        if broadcast_msg != prev_broadcast_msg:
            await hub.ble.broadcast(broadcast_msg);
            timer.reset();
        elif timer.time() > 10000:
            await hub.ble.broadcast(None);
            timer.pause();
            timer.reset();
        
        prev_broadcast_msg = broadcast_msg;
        
        await wait(100);

async def detect_colour():
    global broadcast_msg;
    global current_power;
    timer = StopWatch();

    while True:
        if timer.time() < 500:
            await wait(50);
            continue;

        got_color = await get_colour(sensor);
        if got_color == HSVColor.MEDIUMBLUE:
            hub.light.on(Color.CYAN);
            events.append(Event_Stop_Train);
            timer.reset();

        elif got_color == HSVColor.BLUE:
            hub.light.on(Color.BLUE);
            events.append(Event_Slow_Train);
            timer.reset();

        else:
            await wait(50);

async def handle_events():
    global events;
    global broadcast_msg;
    global current_power;
    global fast_power;
    global slow_power;

    while True:
        if len(events) > 0:
            event = events.pop();
            if event == Event_Stop_Train:
                if current_power > 0:
                    motor.stop();
                    current_power = 0;       
                    broadcast_msg = 'stopped';

            elif event == Event_Slow_Train:
                if current_power > slow_power:
                    await ramp_power(motor, fast_power, slow_power);
                    current_power = slow_power;

            elif event == Event_Start_Train:
                if current_power == 0:
                    broadcast_msg = 'running';
                    await ramp_power(motor, 0, fast_power);
                    current_power = fast_power;
            
            await wait(500);
        else:
            await wait(100);

async def handle_msgs():
    global broadcast_msg;
    global current_power;
    global events;
    timer = StopWatch();

    while True:
        if timer.time() < 2000:
            await wait(50);
            continue;

        data = hub.ble.observe(1)

        if data is not None and data == 'start' and current_power == 0:
            hub.light.on(Color.GREEN);
            events.append(Event_Start_Train);
            timer.reset();
        else:
            await wait(50);


async def main():
    await multitask(handle_msgs(), detect_colour(), handle_broadcast(), handle_events());

run_task(main())
