from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color, Button
from pybricks.tools import wait, StopWatch

from Channels import Channels
from Messages import Messages
from Signal import Signal

class SignalHub(object):
    def __init__(self, direction, point, line_channel, point_channel, use_auto_stop = False):
        self.direction = direction
        self.point = point
        self.line_channel = line_channel
        self.point_channel = point_channel
        self.use_auto_stop = use_auto_stop
        self.auto_stop_timer = StopWatch()
        observe_channels = [line_channel]
        if point_channel is not None:
            observe_channels.append(point_channel)
        self._hub = TechnicHub(observe_channels=tuple(observe_channels))
        self._hub.system.set_stop_button(None)

        self.signal = Signal(Port.A)
        self.timeout_timer = StopWatch()
        self.power = 90
        self._hub.light.on(Color.GREEN)


    def determine_state(self):
        trainData = self._hub.ble.observe(self.line_channel)

        if trainData == self.direction:
            if self.point is None:
                return True

            if self.point_channel is not None:
                pointData = self._hub.ble.observe(self.point_channel)
            else:
                pointData = None

            if pointData == self.point:
                return True
            else:
                return False
        elif trainData is not None:
            return False

        return None

    def run(self):
        pressed = self._hub.buttons.pressed();

        if Button.CENTER in pressed:
            self.signal.set_stop()
            raise SystemExit

        should_go = self.determine_state()
        
        if should_go is True:
            if not self.signal.go and not self.ignore_go:
                self.signal.set_go()
                if self.use_auto_stop:
                    self.auto_stop_timer.reset()
                    self.auto_stop_timer.resume()
        elif should_go is False:
            if self.signal.go:
                self.signal.set_stop()
                if self.use_auto_stop:
                    self.auto_stop_timer.pause()
                    self.auto_stop_timer.reset()
            self.ignore_go = False
        
        if should_go is not None:
            self.timeout_timer.reset()
            self.timeout_timer.resume()

        if self.timeout_timer.time() > 10000:
            if not self.signal.go:
                self.signal.set_go()
        elif self.use_auto_stop and self.auto_stop_timer.time() > 10000:
            if self.signal.go:
                self.signal.set_stop()
                self.ignore_go = True
                self.auto_stop_timer.pause()
                self.auto_stop_timer.reset()
