from pybricks.tools import wait

from Channels import Channels
from PointHub import PointHub

point = PointHub(Channels.BranchPoint, 'termpoint')

while True:
    point.controller()

    wait(100)
