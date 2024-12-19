from pybricks.tools import wait, StopWatch
import Cmds
from TrainHub import TrainHub
import Batches
import Colours
from micropython import mem_info
from pybricks.parameters import Color

print(mem_info())

train = TrainHub()
_MIN_LOOP_INTERVAL = 50


def wait_for_colour(train):
    while True:
        c = train.get_colour()

        if train.get_colour() != Colours.NONE:
            return c

        wait(500)


def init_batch(train):
    colour_code = wait_for_colour(train)
    if colour_code == Colours.SC_KM:
        train.light(Color.BLUE)
        return Batches.get_batch(Batches.KMSTART)
    elif colour_code == Colours.SC_BN:
        train.light(Color.GREEN)
        return Batches.get_batch(Batches.BNSTART)
    elif colour_code == Colours.SC_HIToBN:
        train.light(Color.RED)
        return Batches.get_batch(Batches.HITOBNSTART)

    train.light(Color.YELLOW)
    return Batches.get_batch(Batches.HITOKMSTART)


batch = init_batch(train)
loop_timer = StopWatch()

while True:
    loop_timer.reset()

    train.perform_regular_checks()

    cmd = batch.pop(0)
    print(cmd)
    if cmd[0] == Cmds.WaitMsg:
        # print('wait', train.hub_config.observe_channels, cmd[1])
        while True:
            data = train.observe()
            if len(data) > 0 and data.count(cmd[1]) > 0:
                break
            wait(50)

    elif cmd[0] == Cmds.WaitForColour:
        while True:
            if train.get_colour() == cmd[1]:
                if cmd[1] == Colours.BLUE:
                    train.light(Color.BLUE)
                elif cmd[1] == Colours.RED:
                    train.light(Color.RED)
                elif cmd[1] == Colours.YELLOW:
                    train.light(Color.YELLOW)
                elif cmd[1] == Colours.GREEN:
                    train.light(Color.GREEN)
                wait(50)
                break
            wait(10)

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
        batch += Batches.get_batch(cmd[1])

    t = _MIN_LOOP_INTERVAL - loop_timer.time()
    if t > 0:
        wait(t)
