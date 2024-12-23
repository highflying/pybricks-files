from pybricks.tools import wait, StopWatch
from Messages import Messages
from Colours import HSVColor
from TrainHub import TrainHub
from pybricks.parameters import Color, Button
from pybricks.pupdevices import Remote
from Channels import Channels

train = TrainHub()

if train.hub_config.broadcast_channel == Channels.InnerLoopTrain:
    hub_name = "inner"
else:
    hub_name = "outer"

remote = Remote(name=hub_name)
remote.light.on(Color.GREEN)

DEBUG = False
PAUSE_AFTER_START = 3000
COLOUR_INTERVAL = 1000
STOP_COLOUR = HSVColor.MEDIUMBLUE
SLOW_COLOUR = HSVColor.TEAL
FAST_COLOUR = HSVColor.RED
MIN_LOOP_INTERVAL = 10

colour_timer = StopWatch()
loop_timer = StopWatch()
button_timer = StopWatch()
left_siding = False

while True:
    loop_timer.reset()

    data = train.observe()

    pressed = remote.buttons.pressed()
    if button_timer.time() > 2000:
        pressed = remote.buttons.pressed()

        if Button.LEFT_PLUS in pressed:
            train.fast()
            colour_timer.reset()
            button_timer.reset()

        elif Button.LEFT_MINUS in pressed:
            train.slow()
            colour_timer.reset()
            button_timer.reset()

        elif Button.LEFT in pressed:
            train.stop()
            button_timer.reset()

    data = train.observe()

    if train.is_stopped() and data == Messages.Start:
        train.light(Color.YELLOW)
        train.fast()
        wait(PAUSE_AFTER_START)
        train.light(Color.GREEN)

        if train.is_goods():
            left_siding = True

    elif not train.is_stopped() and colour_timer.time() > COLOUR_INTERVAL:
        got_color = train.get_colour()

        if got_color == STOP_COLOUR:
            colour_timer.reset()
            if DEBUG:
                print(got_color)

            if train.is_passenger():
                if DEBUG:
                    print("stop")
                train.stop()
            elif train.is_goods():
                if DEBUG:
                    print("stop")

                # train.stop()
                # train.light(Color.RED)
                if train.is_reversing():
                    if DEBUG:
                        print("stop")
                    train.stop()
                elif not left_siding:
                    if DEBUG:
                        print("slow")
                    train.slow()

        elif got_color == SLOW_COLOUR:
            if DEBUG:
                print(got_color)
            colour_timer.reset()

            if train.is_passenger():
                if DEBUG:
                    print("slow")
                train.slow()
            elif train.is_goods():
                if left_siding:
                    if DEBUG:
                        print("leftsiding")
                    left_siding = False
                elif train.is_slow():
                    if DEBUG:
                        print("stop and reverse")
                    train.stop_and_reverse()

        elif got_color == FAST_COLOUR:
            if DEBUG:
                print(got_color)

            train.fast()

    # t = MIN_LOOP_INTERVAL - loop_timer.time()
    # if t > 0:
    #     wait(t)
    wait(1)
