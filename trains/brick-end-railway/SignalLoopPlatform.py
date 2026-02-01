from pybricks.tools import wait

from Channels import Channels
from Messages import Messages
from SignalHub import SignalHub

signal = SignalHub(
    Messages.Forward, None, 
    Channels.LoopTrain, None, True)

while True:
    signal.run()

    wait(50)
