from pybricks.hubs import TechnicHub
from pybricks.parameters import Color, Port
from pybricks.tools import wait, StopWatch
from pybricks.pupdevices import ColorDistanceSensor

class HubsClass:
    InnerLoopTrain = 1;
    InnerLoopController = 21;
    OuterLoopTrain = 41;
    OuterLoopController = 61;

Hubs = HubsClass();

# broadcast_channel=Hubs.InnerLoopTrain,
broadcastChannel=Hubs.OuterLoopTrain;
# observe_channels=Hubs.InnerLoopController
observeChannel=Hubs.OuterLoopController

hub = TechnicHub(
    broadcast_channel=broadcastChannel,
    observe_channels=[observeChannel]
)
sensor = ColorDistanceSensor(Port.B)

hub.light.on(Color.GREEN)

DEBUG = True;

# train_status = TrainStatus.Stopped;
# distanceTimer = StopWatch();
broadcastTimer = StopWatch();
isBroadcasting = False;
loopTimer = StopWatch();
prevReceived = None;
trainMoving = False;
trainStarting = False;
lightOff = False;

n = 0;
while True:
    loopTimer.reset();
    # if DEBUG:
    #     n = n + 1;
    #     print('In loop', n);

    if isBroadcasting and broadcastTimer.time() > 3000:
        # if DEBUG:
        print('Finished broadcasting');
        isBroadcasting = False;
        # wait(30);
        hub.ble.broadcast(2);
        # wait(110);
        broadcastTimer.pause();
        hub.light.on(Color.GREEN);

    wait(30);
    data = hub.ble.observe(observeChannel);

    # print(hub.ble.signal_strength(Hubs.InnerLoopController));

    # if DEBUG and data != None and data != prevReceived:
    # print('Received', data);
    #     prevReceived = data;

    if data is not None and prevReceived != data:
        print('Received', data);
        if data == 1 and not trainMoving:
            trainMoving = True;
            trainStarting = False;
            hub.light.on(Color.GREEN);
            # if DEBUG:
            print('Train running');
        elif data == 0 and trainMoving:# and not trainStarting:
        # elif data == Messages.Stopped and train_status != TrainStatus.Stopped:
            trainMoving = False;
            hub.light.on(Color.RED);
            # if DEBUG:
            print('Train stopped');
            # wait(1000);
    prevReceived = data;

    # wait(20)

    # if train_status == TrainStatus.Stopped:
    if not trainMoving and not isBroadcasting:
        # if DEBUG:
        #     print('Not broadcasting so checking distance');
        distance = sensor.distance();
        lightOff = False;
        if distance < 80:
            sensor.light.off();
            # if DEBUG:
            print('Broadcast start')
            # if not isBroadcasting:
            hub.light.blink(Color.YELLOW,[500,500])
            isBroadcasting = True;
            broadcastTimer.reset();
            broadcastTimer.resume();
            # wait(30);
            hub.ble.broadcast(1);
            # wait(110);
            # trainStarting = True;
         
        # else:
        #     hub.ble.broadcast(None);
        #     isBroadcasting = False;
    elif not lightOff:
        sensor.light.off();
        # print('Broadcast none')
        # hub.ble.broadcast(None);
        lightOff = True;
        # wait(30);
    # else:
        # wait(30);

    # elif train_status == TrainStatus.Starting and distanceTimer.time() > 10000:
    # elif broadcastTimer.time() > 10000 and trainStarting:
    #     # train_status = TrainStatus.Stopped;
    #     trainMoving = False
    #     # hub.light.on(Color.RED)
    #     broadcastTimer.pause()
    #     hub.light.on(Color.YELLOW);
    #     if DEBUG:
    #         print('Starting timed out');
    # elif DEBUG:
    #     print('Waiting');

    # elif distanceTimer.time() > 30000:
    #     train_status = TrainStatus.Stopped;
    #     distanceTimer.pause();
    #     if DEBUG:
    #         print('Timed out waiting for train to stop');
    
    t = 20 - loopTimer.time();
    if t > 0:
        # print('Wait extra', t)
        wait(t)

