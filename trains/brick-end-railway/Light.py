from pybricks.pupdevices import Light
from pybricks.tools import wait

class LightController(object):
    def __init__(self, port):
        self.light = Light(port)


    def ghost(self):
        for brightness in range(0, 101, 2):  # Step by 2% for smoother transition
            self.light.on(brightness)
            wait(100)  # 50 steps * 100ms = 5000ms = 5 seconds

        # Stay at full brightness for 10 seconds
        self.light.on(100)
        wait(10000)

        for brightness in range(100, -1, -5):
            self.light.on(brightness)
            wait(100)

        # Ensure light is completely off
        self.light.off()


