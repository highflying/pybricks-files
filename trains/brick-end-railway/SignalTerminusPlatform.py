from pybricks.tools import wait

from Channels import Channels
from Messages import Messages
from SignalHub2 import SignalHub2

signal = SignalHub2(
    Messages.Forward, 
    Channels.BranchLine, Channels.BranchPoint, True)

while True:
    signal.run()

    wait(50)
