from pybricks.tools import wait

from Channels import Channels
from Messages import Messages
from SignalHub import SignalHub

signal = SignalHub(
    Messages.Backward, None, 
    Channels.BranchLine, None, True)

while True:
    signal.run()

    wait(50)
