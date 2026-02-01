from Channels import Channels
from Messages import Messages
from TrainHub import TrainHub, TrainMode

train = TrainHub(Channels.BranchLine, "bercont")
train.set_mode(TrainMode.Branch)
train.run()
