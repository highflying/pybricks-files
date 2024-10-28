from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait, StopWatch
from Channels import Channels
from Messages import Messages
from Colours import HSVColor, get_colour

isGoods = False;
isPassenger = False;

# def get_colour(sensor):
#     color = sensor.hsv();
#     if color.v > 60:
#         # print(color);
#         if color.h > 200 and color.h < 230 and color.s > 30 and color.s< 40:
#             return 'grey';
#         elif color.h > 210 and color.h < 230 and color.s > 90:
#             return 'blue';
#         elif color.h > 210 and color.h < 220 and color.s > 80:
#             return 'mediumblue';
#         elif color.h > 350 and color.h < 360:
#             return 'red';
#         elif color.h > 50 and color.h < 60:
#             return 'yellow';
#         elif color.h > 180 and color.h < 190:
#             return 'teal';
#         elif color.h > 130 and color.h < 140:
#             return 'green';

#     return 'none';

broadcastChannel = Channels.OuterLoopController
observeChannel = Channels.OuterLoopTrain

hub = CityHub()

fast_power = 55
slow_power = 35

if hub.system.name() == 'Autocoach Hub':
    broadcastChannel = Channels.InnerLoopController
    observeChannel = Channels.InnerLoopTrain
    isPassenger = True;
    fast_power = -80
    slow_power = -55
elif hub.system.name() == 'Tram Hub':
    broadcastChannel = Channels.InnerLoopController
    observeChannel = Channels.InnerLoopTrain
    isGoods = True;
    fast_power = -60
    slow_power = -58
elif hub.system.name() == 'White Coach Hub':
    broadcastChannel = Channels.OuterLoopController
    observeChannel = Channels.OuterLoopTrain
    isPassenger = True;
    fast_power = 100
    slow_power = 100

hub = CityHub(
    broadcast_channel=broadcastChannel,
    observe_channels=[observeChannel]
)

motor = DCMotor(Port.A)
sensor = ColorDistanceSensor(Port.B)

hub.light.on(Color.GREEN)
hub.ble.broadcast(Messages.Stopped)

DEBUG = False

current_power = 0
colourTimer = StopWatch()
broadcastTimer = StopWatch()
isBroadcasting = False
reversing = False
leftSiding = False
slowGoods = True
prevReceived = None

def reverseTrain():
    global current_power, leftSiding, reversing

    if current_power != 0:
        if isPassenger or (isGoods and not leftSiding):
            motor.stop()
            current_power = 0
            wait(1000)

            motor.dc(slow_power * -1)
            current_power = slow_power * -1
            reversing = True
        elif isGoods and leftSiding:
            leftSiding = False

def stopTrain():
    global current_power, reversing, isBroadcasting;

    if current_power != 0:
        motor.stop()
        current_power = 0
        reversing = False
        isBroadcasting = True
        hub.ble.broadcast(Messages.Stopped)
        broadcastTimer.reset()
        broadcastTimer.resume()

def slowTrain():
    global current_power;

    if abs(current_power) > abs(slow_power):
        if leftSiding:
            pass
        else:
            motor.dc(slow_power)
            current_power = slow_power

def startTrain():
    global current_power, leftSiding, isBroadcasting;

    if current_power == 0:
        current_power = fast_power
        motor.dc(fast_power)
        isBroadcasting = True
        broadcastTimer.reset()
        broadcastTimer.resume()
        hub.ble.broadcast(Messages.Running)
        wait(10000)

        if isGoods:
            leftSiding = True
    else:
        motor.stop()
        current_power = 0

loopTimer = StopWatch();

while True:
    loopTimer.reset();

    # if isBroadcasting and broadcastTimer.time() > 3000:
    #     # if DEBUG:
    #     print('Finished broadcasting')
    #     # wait(30)
    #     hub.ble.broadcast(2)
    #     # wait(110)
    #     isBroadcasting = False
    #     broadcastTimer.pause()

    data = hub.ble.observe(observeChannel)

    if current_power == 0:
        if data == Messages.Start:
            startTrain()

    if current_power != 0 and colourTimer.time() > 1000:
        got_color = get_colour(sensor)

        if got_color == HSVColor.MEDIUMBLUE:
            colourTimer.reset()
            print('mediumblue')

            if isPassenger:
                stopTrain()
            elif isGoods:
                if reversing:
                    print('stop')
                    stopTrain()
                elif current_power != 0:
                    print('slow')
                    slowTrain()

        elif isPassenger and got_color == HSVColor.TEAL:
            print('teal')
            colourTimer.reset()
            slowTrain()

        elif isGoods and got_color == HSVColor.TEAL:
            print('teal')
            colourTimer.reset()
            if leftSiding:
                print('leftsiding')
                leftSiding = False
            elif current_power == slow_power:
                print('reverse')
                reverseTrain()

    t = 10 - loopTimer.time();
    if t > 0:
        wait(t)

