# from pybricks.hubs import TechnicHub
# from pybricks.pupdevices import Motor
# from pybricks.parameters import Port, Color
from pybricks.tools import wait

from Channels import Channels
from Messages import Messages
from SignalHub import SignalHub

# class SignalHub(object):
#     def __init__(self):
#         self._hub = TechnicHub(observe_channels=[Channels.LoopTrain])
#         self.signal = Signal(Port.A)
#         self.timeout_timer = StopWatch()
#         self.auto_stop_timer = StopWatch()
#         self._hub.light.on(Color.GREEN)
#         self.ignore_go = False

#     def run(self):
#         data = self._hub.ble.observe(Channels.LoopTrain)

#         if data != Messages.Stopped:
#             if not self.signal.go and not self.ignore_go:
#                 self.signal.set_go()
#                 self.auto_stop_timer.reset()
#                 self.auto_stop_timer.resume()
#             self.timeout_timer.reset()
#             self.timeout_timer.resume()
#         elif data == Messages.Stopped:
#             if self.signal.go:
#                 self.signal.set_stop()
#                 self.auto_stop_timer.pause()
#                 self.auto_stop_timer.reset()
#             self.ignore_go = False
#             self.timeout_timer.reset()
#             self.timeout_timer.resume()

#         if self.timeout_timer.time() > 10000:
#             if not self.signal.go:
#                 self.signal.set_go()
#         elif self.auto_stop_timer.time() > 10000:
#             if self.signal.go:
#                 self.signal.set_stop()
#                 self.ignore_go = True
#                 self.auto_stop_timer.pause()
#                 self.auto_stop_timer.reset()

signal = SignalHub(Messages.Forward, None, Channels.LoopTrain, None, True)

while True:
    signal.run()

    wait(50)
