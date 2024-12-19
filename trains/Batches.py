import Constants
import Cmds
import Colours
from micropython import const

InnerLoopBatch = [
    [Cmds.WaitMsg, Constants.Channel_InnerCont, Constants.Msg_Start],
    [Cmds.FastTrain],
    [Cmds.WaitForColour, Colours.TEAL],
    [Cmds.WaitForColour, Colours.TEAL],
    [Cmds.SlowTrain],
    [Cmds.WaitForColour, Colours.MEDIUMBLUE],
    [Cmds.StopTrain],
    [Cmds.StartEmit, Constants.Msg_Stopped],
    [Cmds.AddBatch, "InnerLoop"],
]

InnerSidingBatch = [
    [Cmds.WaitMsg, Constants.Channel_InnerCont, Constants.Msg_Start],
    [Cmds.FastTrain],
    [Cmds.WaitForColour, Colours.TEAL],
    [Cmds.WaitForColour, Colours.TEAL],
    [Cmds.WaitForColour, Colours.MEDIUMBLUE],
    [Cmds.SlowTrain],
    [Cmds.WaitForColour, Colours.TEAL],
    [Cmds.StopTrain],
    [Cmds.ToggleDirection],
    [Cmds.Pause, 1000],
    [Cmds.SlowTrain],
    [Cmds.WaitForColour, Colours.MEDIUMBLUE],
    [Cmds.StopTrain],
    [Cmds.ToggleDirection],
    [Cmds.StartEmit, Constants.Msg_Stopped],
    [Cmds.AddBatch, "InnerSiding"],
]

OuterLoopBatch = [
    [Cmds.WaitMsg, Constants.Channel_OuterCont, Constants.Msg_Start],
    [Cmds.FastTrain],
    [Cmds.WaitForColour, Colours.TEAL],
    [Cmds.SlowTrain],
    [Cmds.WaitForColour, Colours.MEDIUMBLUE],
    [Cmds.StopTrain],
    [Cmds.StartEmit, Constants.Msg_Stopped],
    [Cmds.AddBatch, "OuterLoop"],
]

KMStartBatch = [
    [Cmds.WaitMsg, Constants.Msg_KMArrive],
    [Cmds.StartEmit, Constants.Msg_KMDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "HIToBN"],
]

KMBatch = [
    [Cmds.WaitForColour, Colours.SC_KM],
    [Cmds.StartEmit, Constants.Msg_KMArrive],
    [Cmds.WaitForColour, Colours.SC_KM],
    [Cmds.StopTrain],
    [Cmds.WaitMsg, Constants.Msg_KMDepart],
    [Cmds.ToggleDirection],
    [Cmds.SlowTrain],
    [Cmds.WaitForColour, Colours.SC_KM],
    [Cmds.StopTrain],
    [Cmds.WaitMsg, Constants.Msg_KMArrive],
    [Cmds.StartEmit, Constants.Msg_KMDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "HIToBN"],
]

# HIToKMBatch = [[Cmds.AddBatch, "KM"]]

HIToBNBatch = [
    [Cmds.WaitForColour, Colours.SC_HIToKM],
    [Cmds.SlowTrain],
    [Cmds.WaitForColour, Colours.SC_HIToBN],
    [Cmds.StopTrain],
    [Cmds.StartEmit, Constants.Msg_HIArrive],
    [Cmds.WaitMsg, Constants.Msg_HIDepart],
    [Cmds.StopEmit],
    [Cmds.StartEmit, Constants.Msg_HIDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "BN"],
]

HIToBNStartBatch = [
    [Cmds.StartEmit, Constants.Msg_HIArrive],
    [Cmds.WaitMsg, Constants.Msg_HIDepart],
    [Cmds.StopEmit],
    [Cmds.StartEmit, Constants.Msg_HIDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "BN"],
]

HIToKMBatch = [
    [Cmds.WaitForColour, Colours.SC_HIToBN],
    [Cmds.SlowTrain],
    [Cmds.WaitForColour, Colours.SC_HIToKM],
    [Cmds.StopTrain],
    [Cmds.StartEmit, Constants.Msg_HIArrive],
    [Cmds.WaitMsg, Constants.Msg_HIDepart],
    [Cmds.StopEmit],
    [Cmds.StartEmit, Constants.Msg_HIDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "KM"],
]

HIToKMStartBatch = [
    [Cmds.StartEmit, Constants.Msg_HIArrive],
    [Cmds.WaitMsg, Constants.Msg_HIDepart],
    [Cmds.StopEmit],
    [Cmds.StartEmit, Constants.Msg_HIDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "KM"],
]

# HIToBNBatch = [[Cmds.AddBatch, "BN"]]

BNBatch = [
    [Cmds.WaitForColour, Colours.SC_BN],
    [Cmds.StartEmit, Constants.Msg_BNArrive],
    [Cmds.WaitForColour, Colours.SC_BN],
    [Cmds.StopTrain],
    [Cmds.WaitMsg, Constants.Msg_BNDepart],
    [Cmds.ToggleDirection],
    [Cmds.SlowTrain],
    [Cmds.WaitForColour, Colours.SC_BN],
    [Cmds.StopTrain],
    [Cmds.WaitMsg, Constants.Msg_BNArrive],
    [Cmds.StartEmit, Constants.Msg_BNDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "HIToKM"],
]

BNStartBatch = [
    [Cmds.WaitMsg, Constants.Msg_BNArrive],
    [Cmds.StartEmit, Constants.Msg_BNDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "HIToKM"],
]
