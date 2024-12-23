from pybricks.tools import wait, StopWatch
import Cmds
from TrainHub import TrainHub
import Batches
import Colours
from micropython import mem_info
from pybricks.parameters import Color
import Constants

print(mem_info())

hub = TrainHub()
_MIN_LOOP_INTERVAL = 200

batch = hub.get_initial_batch()
loop_timer = StopWatch()
sensor_timer = StopWatch()

while True:
    loop_timer.reset()

    hub.perform_regular_checks()

    cmd = batch.pop(0)
    print(cmd)
    if cmd[0] == Cmds.WaitMsg:
        sensor_timer.reset()
        sensor_timer.resume()
        hub.broadcast(None)
        while True:
            data = hub.observe()
            if len(data) > 0 and data.count(cmd[1]) > 0:
                break

            if hub.perform_regular_checks():
                break

            if len(cmd) == 3 and sensor_timer.time() > cmd[2]:
                break

            wait(_MIN_LOOP_INTERVAL)

        sensor_timer.pause()

    elif cmd[0] == Cmds.WaitForColour:
        while True:
            if hub.get_colour() == cmd[1]:
                if cmd[1] == Colours.BLUE:
                    hub.light(Color.BLUE)
                elif cmd[1] == Colours.RED:
                    hub.light(Color.RED)
                elif cmd[1] == Colours.YELLOW:
                    hub.light(Color.YELLOW)
                elif cmd[1] == Colours.GREEN:
                    hub.light(Color.GREEN)
                break
            wait(10)

    elif cmd[0] == Cmds.FastTrain:
        hub.fast()

    elif cmd[0] == Cmds.SlowTrain:
        hub.slow()

    elif cmd[0] == Cmds.StopTrain:
        hub.stop()

    elif cmd[0] == Cmds.StartEmit:
        hub.broadcast(cmd[1])

    elif cmd[0] == Cmds.StopEmit:
        hub.broadcast(None)

    elif cmd[0] == Cmds.SetDirection:
        if cmd[1] == Constants.Direction_BN:
            hub.move_backwards()
        else:
            hub.move_forward()

    elif cmd[0] == Cmds.Pause:
        wait(cmd[1])

    elif cmd[0] == Cmds.AddBatch:
        batch += Batches.get_batch(cmd[1])

    elif cmd[0] == Cmds.WaitSensor:
        while True:
            if hub.is_sensor_triggered():
                break
            wait(10)

    elif cmd[0] == Cmds.SensorOff:
        hub.turn_sensor_off()

    t = _MIN_LOOP_INTERVAL - loop_timer.time()
    if t > 0:
        wait(t)
    wait(50)
