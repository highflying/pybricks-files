from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch
from Messages import Messages
from ControllerHub import ControllerHub

DEBUG = False
MIN_LOOP_INTERVAL = 1

loop_timer = StopWatch()
timeout_timer = StopWatch()
train_moving = False

controller = ControllerHub()
controller.light(Color.GREEN)

while True:
    loop_timer.reset()

    data = controller.observe()

    if data is not None:
        if data == Messages.Running and not train_moving:
            train_moving = True
            # controller.light(Color.GREEN)
            controller.stop_broadcasting()
        elif data == Messages.Stopped and train_moving:
            train_moving = False
            # controller.light(Color.RED)

    if train_moving or controller.is_broadcasting:
        controller.sensor_off()
    elif controller.is_sensor_triggered():
        controller.broadcast(Messages.Start)

    if timeout_timer.time() > 30000:
        train_moving = False
        # controller.light(Color.RED)

    # consider having a longer wait when only pinging and waiting for a response?
    t = MIN_LOOP_INTERVAL - loop_timer.time()
    if t > 0:
        wait(t)
