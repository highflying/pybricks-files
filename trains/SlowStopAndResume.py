from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait, StopWatch
from Channels import Channels
from Messages import Messages
from Colours import HSVColor, get_colour

isGoods = False
isPassenger = False

broadcastChannel = Channels.OuterLoopController
observeChannel = Channels.OuterLoopTrain

hub = CityHub()

fast_power = 55
slow_power = 35

if hub.system.name() == "Autocoach Hub":
    broadcastChannel = Channels.OuterLoopController
    observeChannel = Channels.OuterLoopTrain
    isPassenger = True
    fast_power = -55
    slow_power = -35
elif hub.system.name() == "Tram Hub":
    broadcastChannel = Channels.InnerLoopController
    observeChannel = Channels.InnerLoopTrain
    isGoods = True
    fast_power = 55
    slow_power = 35

hub = CityHub(broadcast_channel=broadcastChannel, observe_channels=[observeChannel])

motor = DCMotor(Port.A)
sensor = ColorDistanceSensor(Port.B)

hub.light.on(Color.GREEN)
hub.ble.broadcast(Messages.Stopped)

current_power = 0
colourTimer = StopWatch()
reversing = False
leftSiding = False


def reverseTrain():
    global current_power, leftSiding, reversing

    if current_power > 0:
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
    global current_power, reversing

    if current_power != 0:
        motor.stop()
        current_power = 0
        reversing = False
        hub.ble.broadcast(Messages.Stopped)


def slowTrain():
    global current_power

    if abs(current_power) > abs(slow_power):
        if leftSiding:
            pass
        else:
            motor.dc(slow_power)
            current_power = slow_power


def startTrain():
    global current_power, leftSiding

    if current_power == 0:
        current_power = fast_power
        motor.dc(fast_power)
        hub.ble.broadcast(Messages.Running)

        if isGoods:
            leftSiding = True
    else:
        motor.stop()
        current_power = 0


loopTimer = StopWatch()

while True:
    loopTimer.reset()

    data = hub.ble.observe(observeChannel)

    if current_power == 0:
        if data == Messages.Start:
            startTrain()

    if current_power != 0 and colourTimer.time() > 1000:
        got_color = get_colour(sensor)

        if got_color == HSVColor.MEDIUMBLUE:
            colourTimer.reset()

            if isPassenger:
                stopTrain()
            elif isGoods:
                if reversing:
                    stopTrain()
                elif current_power != 0:
                    slowTrain()

        elif isPassenger and got_color == HSVColor.TEAL:
            colourTimer.reset()
            slowTrain()

        elif isGoods and got_color == HSVColor.TEAL:
            colourTimer.reset()
            reverseTrain()

    t = 20 - loopTimer.time()
    if t > 0:
        wait(t)
