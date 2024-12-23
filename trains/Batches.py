import Constants
import Cmds
import Colours

InnerLoop = [
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

InnerSiding = [
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

OuterLoop = [
    [Cmds.WaitMsg, Constants.Channel_OuterCont, Constants.Msg_Start],
    [Cmds.FastTrain],
    [Cmds.WaitForColour, Colours.TEAL],
    [Cmds.SlowTrain],
    [Cmds.WaitForColour, Colours.MEDIUMBLUE],
    [Cmds.StopTrain],
    [Cmds.StartEmit, Constants.Msg_Stopped],
    [Cmds.AddBatch, "OuterLoop"],
]

KMStart = [
    [Cmds.WaitMsg, Constants.Msg_KMArrive],
    [Cmds.StartEmit, Constants.Msg_KMDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "HIToBN"],
]

KM = [
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

HIToBN = [
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

HIToBNStart = [
    [Cmds.StartEmit, Constants.Msg_HIArrive],
    [Cmds.WaitMsg, Constants.Msg_HIDepart],
    [Cmds.StopEmit],
    [Cmds.StartEmit, Constants.Msg_HIDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "BN"],
]

HIToKM = [
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

HIToKMStart = [
    [Cmds.StartEmit, Constants.Msg_HIArrive],
    [Cmds.WaitMsg, Constants.Msg_HIDepart],
    [Cmds.StopEmit],
    [Cmds.StartEmit, Constants.Msg_HIDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "KM"],
]

BN = [
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

BNStart = [
    [Cmds.WaitMsg, Constants.Msg_BNArrive],
    [Cmds.StartEmit, Constants.Msg_BNDepart],
    [Cmds.FastTrain],
    [Cmds.AddBatch, "HIToKM"],
]
