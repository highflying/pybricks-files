from pybricks.hubs import TechnicHub

hub = TechnicHub(
    broadcast_channel=2,
    observe_channels=[1],
)

n = 1

while True:
    data = hub.ble.observe(1)
    if data is not None:
        print(data)
        hub.ble.broadcast(n)
        n += 2
        # if data[0] == 1:
        #     hub.light.on(5)
        # else:
        #     hub.light.off()
