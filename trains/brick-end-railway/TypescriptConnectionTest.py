from pybricks.hubs import CityHub
from pybricks.pupdevices import Remote, DCMotor, ColorDistanceSensor
from pybricks.parameters import Button, Port, Color
from pybricks.tools import wait, StopWatch
from uerrno import ENODEV, ETIMEDOUT


hub = CityHub(observe_channels=[9])
hub.light.on(Color.GREEN)
# hub.ble.broadcast(4)
timeout = StopWatch();

n = 0
while True:
    received = hub.ble.observe(9)

    if received is not None:
        timeout.reset()

        if received & 0x02:
            hub.light.on(Color.RED)
            wait(100)
        if received & 0x04:
            hub.light.on(Color.YELLOW)
    # print(n, received)
    n = n + 1

    if timeout.time() > 10000:
        hub.light.on(Color.BLUE)

    wait(150)
    # hub.ble.broadcast(2)
    # wait(1000)
    # hub.ble.broadcast(3)
