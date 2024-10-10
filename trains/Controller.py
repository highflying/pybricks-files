from pybricks.hubs import TechnicHub
from pybricks.parameters import Color, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait, multitask, run_task, StopWatch
from pybricks.pupdevices import ColorDistanceSensor

hub = TechnicHub(broadcast_channel=1,observe_channels=[2])
sensor = ColorDistanceSensor(Port.B)

train_status = 'stopped';
hub.light.on(Color.RED)
prev_train_status = 'stopped'

broadcast_msg = None

async def handle_broadcast():
    global broadcast_msg;
    prev_broadcast_msg = None;
    timer = StopWatch();

    while True:
        if broadcast_msg != None:
            prev_broadcast_msg = broadcast_msg;
            await hub.ble.broadcast(broadcast_msg);
            broadcast_msg = None;
            timer.reset();
            timer.resume();
        elif timer.time() > 5000:
            await hub.ble.broadcast(None);
            timer.pause();
            timer.reset();
                
        await wait(100);


async def detect_distance():
    global train_status;
    global broadcast_msg;
    timer = StopWatch();

    while True:
        if timer.time() < 10000:
            await wait(50);
            continue;

        if train_status == 'stopped':
            distance = await sensor.distance();
            if distance < 80:
                await sensor.light.off();
                broadcast_msg = 'start';
                train_status = 'starting'
                timer.reset();
                hub.light.on(Color.YELLOW)

        elif train_status == 'starting':
            if timer.time() > 10000:
                train_status = 'stopped';
                hub.light.on(Color.RED);
        
        await wait(200);

async def handle_msgs():
    global train_status;
    timer = StopWatch();

    while True:
        if timer.time() < 500:
            await wait(500);
            continue;

        data = hub.ble.observe(2);

        if data is not None:
            timer.reset();
            if data == 'running' and train_status != 'running':
                train_status = 'running'
                hub.light.on(Color.GREEN)
            elif data == 'stopped' and train_status != 'stopped' and train_status != 'starting':
                train_status = 'stopped'
                hub.light.on(Color.RED)
        
        await wait(100);

async def main():
    await multitask(handle_msgs(), detect_distance(), handle_broadcast())

run_task(main())
