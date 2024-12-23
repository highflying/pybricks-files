from pybricks.hubs import CityHub

hub = CityHub(
    broadcast_channel=1,
    observe_channels=[2],
)

n = 0

while True:
    data = hub.ble.observe(2)
    if data is not None:
        print(data)
        hub.ble.broadcast(n)
        n += 2
        # if data[0] == 1:
        #     hub.light.on(5)
        # else:
        #     hub.light.off()
