from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color, Button
from pybricks.tools import wait, StopWatch
from uerrno import ENODEV

from Channels import Channels
from Messages import Messages

class LevelCrossingHub(object):
    def __init__(self):
        self._hub = TechnicHub(observe_channels=[Channels.LoopTrain])
        self._motor = Motor(Port.A)
        self.timeout_timer = StopWatch()
        self.auto_open_timer = StopWatch()

        self.power = 480
        self.degrees = 1300
        # self.degrees = 500

        self._hub.light.on(Color.GREEN)
        self.open = False
        self.ignore_close = False
        self._hub.system.set_stop_button(None)

    def open_gates(self):
        self._motor.run_angle(self.power, self.degrees)
        self.open = True

    def close_gates(self):
        self._motor.run_angle(self.power, self.degrees * -1)
        self.open = False

    def run(self):
        pressed = self._hub.buttons.pressed();

        if Button.CENTER in pressed:
            if self.open:
                self.close_gates()
            raise SystemExit

        data = self._hub.ble.observe(Channels.LoopTrain)

        if data is not None:
            self.timeout_timer.reset()
            self.timeout_timer.resume()

            if data == Messages.Stopped:
                # print('Received stopped')
                if not self.open:
                    self.open_gates()
                    self.auto_open_timer.pause()
                    self.auto_open_timer.reset()
                self.ignore_close = False
            elif data == Messages.Forward or data == Messages.Backward or data == Messages.ForwardStart or data == Messages.BackwardStart:
                if data == Messages.ForwardStart or data == Messages.BackwardStart:
                    self.ignore_close = False

                # print('Received moving')
                if self.open and not self.ignore_close:
                    self.close_gates()
                    self.auto_open_timer.reset()
                    self.auto_open_timer.resume()
            # else:
            #     print('Received other')

        if self.timeout_timer.time() > 10000:
            if self.open:
                self.close_gates()
                self.auto_open_timer.pause()
                self.auto_open_timer.reset()
            self.timeout_timer.pause()
            self.timeout_timer.reset()

        if self.auto_open_timer.time() > 10000:
            if not self.open:
                self.open_gates()
            self.ignore_close = True
            self.auto_open_timer.pause()
            self.auto_open_timer.reset()

level_crossing = LevelCrossingHub()

while True:
    level_crossing.run()

    wait(50)
