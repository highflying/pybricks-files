from pybricks.parameters import Color
from micropython import mem_info
import Constants
import Batches
from TrainHub import TrainHub
from BatchedTrain import run_batch

print(mem_info())

hub_config = [
    Constants.Channel_OuterCont,
    [Constants.Channel_OuterTrain],
    0,
    0,
    None,
    Color.GREEN,
    Batches.OUTER_CONTROLLER,
]

hub = TrainHub(hub_config)
initial_batch = Batches.get_batch(hub_config[Constants.HC_InitialBatch])

run_batch(hub, initial_batch)
