import Constants
import Cmds
import Colours

INNERLOOP = 1
INNERSIDING = 2
OUTERLOOP = 3
KMSTART = 4
KM = 5
HITOBN = 6
HITOBNSTART = 7
BN = 8
BNSTART = 9
HITOKM = 10
HITOKMSTART = 11


def get_batch(id):
    if id == INNERLOOP:
        return [
            [Cmds.WaitMsg, Constants.Channel_InnerCont, Constants.Msg_Start],
            [Cmds.FastTrain],
            [Cmds.WaitForColour, Colours.TEAL],
            [Cmds.WaitForColour, Colours.TEAL],
            [Cmds.SlowTrain],
            [Cmds.WaitForColour, Colours.MEDIUMBLUE],
            [Cmds.StopTrain],
            [Cmds.StartEmit, Constants.Msg_Stopped],
            [Cmds.AddBatch, INNERLOOP],
        ]
    elif id == INNERSIDING:
        return [
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
            [Cmds.AddBatch, INNERSIDING],
        ]
    elif id == OUTERLOOP:
        return [
            [Cmds.WaitMsg, Constants.Channel_OuterCont, Constants.Msg_Start],
            [Cmds.FastTrain],
            [Cmds.WaitForColour, Colours.TEAL],
            [Cmds.SlowTrain],
            [Cmds.WaitForColour, Colours.MEDIUMBLUE],
            [Cmds.StopTrain],
            [Cmds.StartEmit, Constants.Msg_Stopped],
            [Cmds.AddBatch, OUTERLOOP],
        ]
    elif id == KMSTART:
        return [
            [Cmds.WaitMsg, Constants.Msg_KMArrive],
            [Cmds.StartEmit, Constants.Msg_KMDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, HITOBN],
        ]
    elif id == KM:
        return [
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
            [Cmds.AddBatch, HITOBN],
        ]
    elif id == HITOBN:
        return [
            [Cmds.WaitForColour, Colours.SC_HIToKM],
            [Cmds.SlowTrain],
            [Cmds.WaitForColour, Colours.SC_HIToBN],
            [Cmds.StopTrain],
            [Cmds.StartEmit, Constants.Msg_HIArrive],
            [Cmds.WaitMsg, Constants.Msg_HIDepart],
            [Cmds.StopEmit],
            [Cmds.StartEmit, Constants.Msg_HIDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, BN],
        ]
    elif id == HITOBNSTART:
        return [
            [Cmds.StartEmit, Constants.Msg_HIArrive],
            [Cmds.WaitMsg, Constants.Msg_HIDepart],
            [Cmds.StopEmit],
            [Cmds.StartEmit, Constants.Msg_HIDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, BN],
        ]
    elif id == BN:
        return [
            [Cmds.WaitForColour, Colours.SC_HIToBN],
            [Cmds.SlowTrain],
            [Cmds.WaitForColour, Colours.SC_HIToKM],
            [Cmds.StopTrain],
            [Cmds.StartEmit, Constants.Msg_HIArrive],
            [Cmds.WaitMsg, Constants.Msg_HIDepart],
            [Cmds.StopEmit],
            [Cmds.StartEmit, Constants.Msg_HIDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, KM],
        ]
    elif id == BNSTART:
        return [
            [Cmds.StartEmit, Constants.Msg_HIArrive],
            [Cmds.WaitMsg, Constants.Msg_HIDepart],
            [Cmds.StopEmit],
            [Cmds.StartEmit, Constants.Msg_HIDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, KM],
        ]
    elif id == BN:
        return [
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
            [Cmds.AddBatch, HITOKM],
        ]
    elif id == BNSTART:
        return [
            [Cmds.WaitMsg, Constants.Msg_BNArrive],
            [Cmds.StartEmit, Constants.Msg_BNDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, HITOKM],
        ]

    print("Unknown batch", id)
    return []
