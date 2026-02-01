from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color, Button
from pybricks.tools import wait, StopWatch

from Channels import Channels
from Messages import Messages
from Signal import Signal

class SignalHub2(object):
    def __init__(self, direction, line_channel, point_channel, use_auto_stop = False):
        self.direction = direction
        self.line_channel = line_channel
        self.point_channel = point_channel
        self.use_auto_stop = use_auto_stop
        self.auto_stop_timer = StopWatch()
        self.ignoreGoStraight = False
        self.ignoreGoDivergent = False
        observe_channels = [line_channel]
        if point_channel is not None:
            observe_channels.append(point_channel)
        self._hub = TechnicHub(observe_channels=tuple(observe_channels))
        self._hub.system.set_stop_button(None)

        self.signalStraight = Signal(Port.B)
        self.signalDivergent = Signal(Port.A)
        self.timeout_timer = StopWatch()
        self.power = 90
        self._hub.light.on(Color.GREEN)


    def determine_state(self):
        trainData = self._hub.ble.observe(self.line_channel)

        if trainData == self.direction:
            pointData = self._hub.ble.observe(self.point_channel)

            if pointData is None:
                return [True,True]
                
            if pointData == Messages.Straight:
                return [True,False]
            
            if pointData == Messages.Divergent:
                return [False,True]
        elif trainData is not None:
            return [False,False]

        return None

    def run(self):
        pressed = self._hub.buttons.pressed();

        if Button.CENTER in pressed:
            self.signalStraight.set_stop()
            self.signalDivergent.set_stop()
            raise SystemExit

        should_go = self.determine_state()
        
        if should_go is not None:
            if should_go[0] is True:
                if not self.signalStraight.go and not self.ignoreGoStraight:
                    self.signalStraight.set_go()
                    if self.use_auto_stop:
                        self.auto_stop_timer.reset()
                        self.auto_stop_timer.resume()
            if should_go[1] is True:
                if not self.signalDivergent.go and not self.ignoreGoDivergent:
                    self.signalDivergent.set_go()
                    if self.use_auto_stop:
                        self.auto_stop_timer.reset()
                        self.auto_stop_timer.resume()
            if should_go[0] is False:
                if self.signalStraight.go:
                    self.signalStraight.set_stop()
                    if self.use_auto_stop:
                        self.auto_stop_timer.pause()
                        self.auto_stop_timer.reset()
                self.ignoreGoStraight = False
            if should_go[1] is False:
                if self.signalDivergent.go:
                    self.signalDivergent.set_stop()
                    if self.use_auto_stop:
                        self.auto_stop_timer.pause()
                        self.auto_stop_timer.reset()
                self.ignoreGoDivergent = False

        if should_go is not None:
            self.timeout_timer.reset()
            self.timeout_timer.resume()

        if self.timeout_timer.time() > 10000:
            self.signalStraight.set_go()
            self.signalDivergent.set_go()

        elif self.use_auto_stop and self.auto_stop_timer.time() > 10000:
            if self.signalStraight.go:
                self.signalStraight.set_stop()
                self.ignoreGoStraight = True
                self.auto_stop_timer.pause()
                self.auto_stop_timer.reset()
            if self.signalDivergent.go:
                self.signalDivergent.set_stop()
                self.ignoreGoDivergent = True
                self.auto_stop_timer.pause()
                self.auto_stop_timer.reset()
