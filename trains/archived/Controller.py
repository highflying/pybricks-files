from pybricks.tools import wait, StopWatch
import Constants
from ControllerHub import ControllerHub
from micropython import mem_info

print(mem_info())

_MIN_LOOP_INTERVAL = 1

loop_timer = StopWatch()
timeout_timer = StopWatch()
train_moving = False

controller = ControllerHub()

started_message = Constants.Msg_HIDepart
stopped_message = Constants.Msg_HIArrive

while True:
    loop_timer.reset()

    data = controller.observe()

    if len(data) > 0:
        if data.count(started_message) > 0 and not train_moving:
            train_moving = True
            controller.stop_broadcasting()
        elif data.count(stopped_message) > 0 and train_moving:
            train_moving = False

    if train_moving or controller.is_broadcasting:
        controller.turn_sensor_off()
    elif controller.is_sensor_triggered():
        print("trigger")
        controller.broadcast(started_message)

    if timeout_timer.time() > 30000:
        train_moving = False

    # consider having a longer wait when only pinging and waiting for a response?
    t = _MIN_LOOP_INTERVAL - loop_timer.time()
    if t > 0:
        wait(t)
