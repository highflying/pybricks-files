from pybricks.tools import wait

from Channels import Channels
from Messages import Messages
from SignalHub import SignalHub

signal = SignalHub(
    Messages.Forward, Messages.Straight, 
    Channels.BranchLine, Channels.BranchPoint, False)

while True:
    signal.run()

    wait(50)
