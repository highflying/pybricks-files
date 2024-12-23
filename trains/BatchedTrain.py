from pybricks.tools import wait
import Cmds
from TrainHub import TrainHub
import Batches
import Colours
from micropython import mem_info

print(mem_info())

train = TrainHub()


def wait_for_colour(train):
    while True:
        c = train.get_colour()

        if train.get_colour() != Colours.NONE:
            return c

        wait(500)


def init_batch(train):
    colour_code = wait_for_colour(train)
    if colour_code == Colours.SC_KM:
        print("km")
        return Batches.KMStart
    elif colour_code == Colours.SC_BN:
        print("bn")
        return Batches.BNStart
    elif colour_code == Colours.SC_HIToBN:
        print("hitobn")
        return Batches.HIToBNStart

    print("hitokm")
    return Batches.HIToKMStart


batch = init_batch(train)

while True:
    train.perform_regular_checks()

    cmd = batch.pop(0)
    print(cmd)
    if cmd[0] == Cmds.WaitMsg:
        # print('wait', train.hub_config.observe_channels, cmd[1])
        while True:
            data = train.observe()
            if len(data) > 0 and data.count(cmd[1]) > 0:
                break
            wait(5)

    elif cmd[0] == Cmds.WaitForColour:
        while True:
            if train.get_colour() == cmd[1]:
                break
            wait(5)

    elif cmd[0] == Cmds.FastTrain:
        train.fast()

    elif cmd[0] == Cmds.SlowTrain:
        train.slow()

    elif cmd[0] == Cmds.StopTrain:
        train.stop()

    elif cmd[0] == Cmds.StartEmit:
        train.broadcast(cmd[1])

    elif cmd[0] == Cmds.StopEmit:
        train.broadcast(None)

    elif cmd[0] == Cmds.ToggleDirection:
        train.toggle_direction()

    elif cmd[0] == Cmds.Pause:
        wait(cmd[1])

    elif cmd[0] == Cmds.AddBatch:
        if cmd[1] == "InnerLoop":
            batch += Batches.InnerLoop
        elif cmd[1] == "InnerSiding":
            batch += Batches.InnerSiding
        elif cmd[1] == "OuterLoop":
            batch += Batches.OuterLoop
        elif cmd[1] == "KMStart":
            batch += Batches.KMStart
        elif cmd[1] == "KM":
            batch += Batches.KM
        elif cmd[1] == "HIToKM":
            batch += Batches.HIToKM
        elif cmd[1] == "HIToBN":
            batch += Batches.HIToBN
        elif cmd[1] == "BN":
            batch += Batches.BN
        elif cmd[1] == "BNStart":
            batch += Batches.BNStart
        else:
            print("Unknown batch", cmd[1])

    wait(1)
