from pybricks.hubs import TechnicHub
from pybricks.parameters import Color, Port
from pybricks.tools import wait, StopWatch
from pybricks.pupdevices import ColorDistanceSensor
from Channels import Channels
from Messages import Messages

broadcastChannel=Channels.InnerLoopTrain;
observeChannel=Channels.InnerLoopController

hub = TechnicHub()

if hub.system.name() == 'Outer Loop Cont':
    broadcastChannel=Channels.OuterLoopTrain;
    observeChannel=Channels.OuterLoopController
elif hub.system.name() == 'Controller Hub':
    broadcastChannel=Channels.InnerLoopTrain;
    observeChannel=Channels.InnerLoopController

hub = TechnicHub(
    broadcast_channel=broadcastChannel,
    observe_channels=[observeChannel]
)

sensor = ColorDistanceSensor(Port.D)

hub.light.on(Color.GREEN)

DEBUG = False;

broadcastTimer = StopWatch();
isBroadcasting = False;
loopTimer = StopWatch();
prevReceived = None;
trainMoving = False;
lightOff = False;

while True:
    loopTimer.reset();

    if isBroadcasting and broadcastTimer.time() > 3000:
        isBroadcasting = False;
        hub.ble.broadcast(Messages.Ping);
        broadcastTimer.pause();
        hub.light.on(Color.GREEN);

    data = hub.ble.observe(observeChannel);

    if data is not None and prevReceived != data:
        if data == Messages.Running and not trainMoving:
            trainMoving = True;
            hub.light.on(Color.GREEN);
        elif data == Messages.Stopped and trainMoving:
            trainMoving = False;
            hub.light.on(Color.RED);

    prevReceived = data;

    if not trainMoving and not isBroadcasting:
        distance = sensor.distance();
        lightOff = False;
        if distance < 80:
            sensor.light.off();
            hub.light.blink(Color.YELLOW,[500,500])
            isBroadcasting = True;
            broadcastTimer.reset();
            broadcastTimer.resume();
            hub.ble.broadcast(Messages.Start);
    elif not lightOff:
        sensor.light.off();
        lightOff = True;

    # consider having a longer wait when only pinging and waiting for a response?
    t = 50 - loopTimer.time();
    if t > 0:
        wait(t)

