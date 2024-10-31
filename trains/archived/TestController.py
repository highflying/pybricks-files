from pybricks.hubs import TechnicHub
from pybricks.parameters import Color, Port
from pybricks.tools import wait, StopWatch
from pybricks.pupdevices import ColorDistanceSensor
from Channels import Channels

hub = TechnicHub(
    broadcast_channel=Channels.InnerLoopTrain,
)
sensor = ColorDistanceSensor(Port.B)

hub.light.on(Color.GREEN)

DEBUG = True

broadcastTimer = StopWatch()
isBroadcasting = False
loopTimer = StopWatch()
codeTimer = StopWatch()
prevReceived = None
prevColor = "blue"

while True:
    loopTimer.reset()

    if isBroadcasting and broadcastTimer.time() > 1000:
        if DEBUG:
            print("Finished broadcasting")

        hub.ble.broadcast(None)  # type: ignore
        isBroadcasting = False
        broadcastTimer.pause()

    if broadcastTimer.time() > 1000:

        distance = sensor.distance()
        if distance < 80:
            codeTimer.reset()
            sensor.light.off()
            if prevColor == "blue":
                hub.light.on(Color.RED)
                hub.ble.broadcast(0)
                prevColor = "red"
            else:
                hub.light.on(Color.BLUE)
                hub.ble.broadcast(1)
                prevColor = "blue"
            isBroadcasting = True
            broadcastTimer.reset()
            broadcastTimer.resume()
            print("Code took", codeTimer.time())

    wait(50)
    t = loopTimer.time()
    if t > 51:
        print("Loop took", t)
