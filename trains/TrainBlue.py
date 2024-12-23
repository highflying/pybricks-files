from pybricks.parameters import Color
from micropython import mem_info
import Constants
from TrainHub import TrainHub
from BatchedTrain import run_batch
from Highley import get_init_batch

print(mem_info())

hub_config = [
    Constants.Channel_BlueTrain,
    [
        Constants.Channel_RedTrain,
        Constants.Channel_GreenTrain,
        Constants.Channel_HIController,
    ],
    -60,
    -40,
    "blue",
    Color.BLUE,
]

hub = TrainHub(hub_config)
initial_batch = get_init_batch(hub)

run_batch(hub, initial_batch)