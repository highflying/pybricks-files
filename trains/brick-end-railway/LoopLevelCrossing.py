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
        self.timeout_timer.pause()
        self.timeout_timer.reset()
        self.auto_open_timer = StopWatch()
        self.auto_open_timer.pause()
        self.auto_open_timer.reset()

        self.power = 480
        self.degrees = 1300
        # self.degrees = 500

        self._motor.reset_angle(0)  # current position = closed

        self._hub.light.on(Color.GREEN)
        self.open = False
        self.gate_moving = False
        self.ignore_close = False
        self._hub.system.set_stop_button(None)

    def open_gates(self):
        if self.open and not self.gate_moving:
            return  # already fully open
        self._motor.run_target(self.power, self.degrees, wait=False)
        self.gate_moving = True
        self.open = True  # intended state

    def close_gates(self):
        if not self.open and not self.gate_moving:
            return  # already fully closed
        self._motor.run_target(self.power, 0, wait=False)
        self.gate_moving = True
        self.open = False  # intended state

    def run(self):
        # Check if gate movement has completed
        if self.gate_moving and self._motor.done():
            self.gate_moving = False

        pressed = self._hub.buttons.pressed();

        if Button.CENTER in pressed:
            self._motor.run_target(self.power, 0)  # blocking close before exit
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
