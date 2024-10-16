from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait, StopWatch

ChannelInnerLoopTrain = 1;
ChannelInnerLoopController = 21;
ChannelOuterLoopTrain = 41;
ChannelOuterLoopController = 61;

isGoods = False;
isPassenger = True;

def get_colour(sensor):
    color = sensor.hsv();
    if color.v > 60:
        # print(color);
        if color.h > 200 and color.h < 230 and color.s > 30 and color.s< 40:
            return 'grey';
        elif color.h > 210 and color.h < 230 and color.s > 90:
            return 'blue';
        elif color.h > 210 and color.h < 220 and color.s > 80:
            return 'mediumblue';
        elif color.h > 350 and color.h < 360:
            return 'red';
        elif color.h > 50 and color.h < 60:
            return 'yellow';
        elif color.h > 180 and color.h < 190:
            return 'teal';
        elif color.h > 130 and color.h < 140:
            return 'green';

    return 'none';

broadcastChannel = ChannelOuterLoopController
observeChannel = ChannelOuterLoopTrain

hub = CityHub(
    broadcast_channel=broadcastChannel,
    observe_channels=[observeChannel]
)

motor = DCMotor(Port.A)
sensor = ColorDistanceSensor(Port.B)

fast_power = 55
slow_power = 35

hub.light.on(Color.GREEN)
# hub.ble.broadcast(False)

DEBUG = True

current_power = 0
colourTimer = StopWatch()
broadcastTimer = StopWatch()
isBroadcasting = False
reversing = False
leftSiding = False
prevReceived = None

def reverseTrain():
    global current_power, leftSiding, reversing

    if current_power > 0:
        if isPassenger or (isGoods and not leftSiding):
            # if DEBUG:
            #     print('Stopping and reversing train')

            motor.stop()
            current_power = 0
            # wait(100)

            motor.dc(slow_power * -1)
            current_power = slow_power * -1
            reversing = True
            # lightOff = False
        elif isGoods and leftSiding:
            # if DEBUG:
            #     print('Not left siding')
            leftSiding = False
    #     elif DEBUG:
    #         print('not here either')
    # elif DEBUG:
    #     print('Already stopped, not reversing')

def stopTrain():
    global current_power, reversing, isBroadcasting;

    if current_power != 0:
        # if DEBUG:
        #     print('Stopping train')
        motor.stop()
        current_power = 0
        reversing = False
        isBroadcasting = True
        wait(30)
        hub.ble.broadcast(0)
        broadcastTimer.reset()
        broadcastTimer.resume()
        wait(110)

    # elif DEBUG:
    #     print('Already stopped')

def slowTrain():
    global current_power;

    if current_power > slow_power:
        if leftSiding:
            pass
            # if DEBUG:
            #     print('Ignoring slow')
        else:
            # if DEBUG:
            #     print('Slowing train')
            motor.dc(slow_power)
            current_power = slow_power
            # lightOff = False
    # elif DEBUG:
    #     print('Already slow')

def startTrain():
    global current_power, leftSiding, isBroadcasting;

    if current_power == 0:
        # if DEBUG:
        #     print('Starting train')
        current_power = fast_power
        motor.dc(fast_power)
        isBroadcasting = True
        broadcastTimer.reset()
        broadcastTimer.resume()
        wait(30)
        hub.ble.broadcast(1)
        wait(100)
 
        # lightOff = False
        if isGoods:
            # if DEBUG:
            #     print('Left siding')
            leftSiding = True
    else:
        # if DEBUG:
        #     print('Stopping train again?')
        motor.stop()
        current_power = 0

loopTimer = StopWatch();
n = 0
while True:
    loopTimer.reset();
    # if DEBUG:
    #     n = n + 1
    #     print('In loop', n, current_power)

    # event = ''

    # if isBroadcasting and broadcastTimer.time() > 3000:
    #     # if DEBUG:
    #     print('Finished broadcasting')
    #     # wait(30)
    #     hub.ble.broadcast(2)
    #     # wait(110)
    #     isBroadcasting = False
    #     broadcastTimer.pause()

    # wait(30);
    data = hub.ble.observe(observeChannel)

    if current_power == 0:
        # if DEBUG and data is not None: # and data != prevReceived:
        # if data is not None:
        # print('Received', data)
        #     prevReceived = data
        if data == 1:
            # if DEBUG:
            #     print('Got start')
            # event = 'start'
            startTrain()
    
    # wait(50)

    # got_color = get_colour(sensor)

    if current_power != 0 and colourTimer.time() > 1000:
        got_color = get_colour(sensor)

        if got_color == 'mediumblue':
            # if DEBUG:
            print('Got mediumblue')
            colourTimer.reset()

            if isPassenger:
                # event = 'stop'
                stopTrain()
            elif isGoods:
                if reversing:
                    # event = 'stop'
                    stopTrain()
                elif current_power != 0:
                    # event = 'slow'
                    slowTrain()
                # else:
                #     print('Should not be here')

        elif isPassenger and got_color == 'teal':
            # if DEBUG:
            print('Got teal')
            # event = 'slow'
            colourTimer.reset()
            slowTrain()

        elif isGoods and got_color == 'teal':
            # if DEBUG:
            #     print('Got teal')
            # event = 'reverse'
            colourTimer.reset()
            reverseTrain()

        # elif DEBUG and got_color != 'none':
        #     print('Got', got_color);
    # elif current_power == 0:
    #     print('Extra wait')
    #     wait(500);

    t = 10 - loopTimer.time();
    if t > 0:
        # print('Wait extra', t)
        wait(t)

