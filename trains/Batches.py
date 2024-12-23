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
    # if id == INNERLOOP:
    #     return [
    #         [Cmds.WaitMsg, Constants.Channel_InnerCont, Constants.Msg_Start],
    #         [Cmds.FastTrain],
    #         [Cmds.WaitForColour, Colours.TEAL],
    #         [Cmds.WaitForColour, Colours.TEAL],
    #         [Cmds.SlowTrain],
    #         [Cmds.WaitForColour, Colours.MEDIUMBLUE],
    #         [Cmds.StopTrain],
    #         [Cmds.StartEmit, Constants.Msg_Stopped],
    #         [Cmds.AddBatch, INNERLOOP],
    #     ]
    # elif id == INNERSIDING:
    #     return [
    #         [Cmds.WaitMsg, Constants.Channel_InnerCont, Constants.Msg_Start],
    #         [Cmds.FastTrain],
    #         [Cmds.WaitForColour, Colours.TEAL],
    #         [Cmds.WaitForColour, Colours.TEAL],
    #         [Cmds.WaitForColour, Colours.MEDIUMBLUE],
    #         [Cmds.SlowTrain],
    #         [Cmds.WaitForColour, Colours.TEAL],
    #         [Cmds.StopTrain],
    #         [Cmds.ToggleDirection],
    #         [Cmds.Pause, 1000],
    #         [Cmds.SlowTrain],
    #         [Cmds.WaitForColour, Colours.MEDIUMBLUE],
    #         [Cmds.StopTrain],
    #         [Cmds.ToggleDirection],
    #         [Cmds.StartEmit, Constants.Msg_Stopped],
    #         [Cmds.AddBatch, INNERSIDING],
    #     ]
    # elif id == OUTERLOOP:
    #     return [
    #         [Cmds.WaitMsg, Constants.Channel_OuterCont, Constants.Msg_Start],
    #         [Cmds.FastTrain],
    #         [Cmds.WaitForColour, Colours.TEAL],
    #         [Cmds.SlowTrain],
    #         [Cmds.WaitForColour, Colours.MEDIUMBLUE],
    #         [Cmds.StopTrain],
    #         [Cmds.StartEmit, Constants.Msg_Stopped],
    #         [Cmds.AddBatch, OUTERLOOP],
    #     ]
    if id == KMSTART:
        return [
            [Cmds.SetDirection, Constants.Direction_KM],
            [Cmds.WaitMsg, Constants.Msg_KMArrive],
            [Cmds.StartEmit, Constants.Msg_KMDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, HITOBN],
        ]
    elif id == KM:
        return [
            [Cmds.SetDirection, Constants.Direction_KM],
            [Cmds.WaitForColour, Colours.SC_KM],
            [Cmds.StartEmit, Constants.Msg_KMArrive],
            [Cmds.Pause, 1000],
            [Cmds.WaitForColour, Colours.SC_KM],
            [Cmds.StopTrain],
            [Cmds.WaitMsg, Constants.Msg_KMDepart],
            [Cmds.SetDirection, Constants.Direction_BN],
            [Cmds.SlowTrain],
            [Cmds.Pause, 2000],
            [Cmds.WaitForColour, Colours.SC_KM],
            [Cmds.StopTrain],
            [Cmds.WaitMsg, Constants.Msg_KMArrive],
            [Cmds.StartEmit, Constants.Msg_KMDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, HITOBN],
        ]
    elif id == HITOBN:
        return [
            [Cmds.SetDirection, Constants.Direction_BN],
            [Cmds.WaitForColour, Colours.SC_HIToKM],
            [Cmds.SlowTrain],
            [Cmds.Pause, 1000],
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
            [Cmds.SetDirection, Constants.Direction_BN],
            [Cmds.StartEmit, Constants.Msg_HIArrive],
            [Cmds.WaitMsg, Constants.Msg_HIDepart],
            [Cmds.StopEmit],
            [Cmds.StartEmit, Constants.Msg_HIDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, BN],
        ]
    # elif id == HITOBN:
    #     return [
    #         [Cmds.WaitForColour, Colours.SC_HIToBN],
    #         [Cmds.SlowTrain],
    #         [Cmds.WaitForColour, Colours.SC_HIToKM],
    #         [Cmds.StopTrain],
    #         [Cmds.StartEmit, Constants.Msg_HIArrive],
    #         [Cmds.WaitMsg, Constants.Msg_HIDepart],
    #         [Cmds.StopEmit],
    #         [Cmds.StartEmit, Constants.Msg_HIDepart],
    #         [Cmds.FastTrain],
    #         [Cmds.AddBatch, KM],
    #     ]
    elif id == HITOKM:
        return [
            [Cmds.SetDirection, Constants.Direction_KM],
            [Cmds.WaitForColour, Colours.SC_HIToBN],
            [Cmds.SlowTrain],
            [Cmds.Pause, 1000],
            [Cmds.WaitForColour, Colours.SC_HIToKM],
            [Cmds.StopTrain],
            [Cmds.StartEmit, Constants.Msg_HIArrive],
            [Cmds.WaitMsg, Constants.Msg_HIDepart],
            [Cmds.StopEmit],
            [Cmds.StartEmit, Constants.Msg_HIDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, KM],
        ]
    elif id == HITOKMSTART:
        return [
            [Cmds.SetDirection, Constants.Direction_KM],
            [Cmds.StartEmit, Constants.Msg_HIArrive],
            [Cmds.WaitMsg, Constants.Msg_HIDepart],
            [Cmds.StopEmit],
            [Cmds.StartEmit, Constants.Msg_HIDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, KM],
        ]
    elif id == BN:
        return [
            [Cmds.SetDirection, Constants.Direction_BN],
            [Cmds.WaitForColour, Colours.SC_BN],
            [Cmds.StartEmit, Constants.Msg_BNArrive],
            [Cmds.Pause, 1000],
            [Cmds.WaitForColour, Colours.SC_BN],
            [Cmds.StopTrain],
            [Cmds.WaitMsg, Constants.Msg_BNDepart],
            [Cmds.SetDirection, Constants.Direction_KM],
            [Cmds.SlowTrain],
            [Cmds.Pause, 2000],
            [Cmds.WaitForColour, Colours.SC_BN],
            [Cmds.StopTrain],
            [Cmds.WaitMsg, Constants.Msg_BNArrive],
            [Cmds.StartEmit, Constants.Msg_BNDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, HITOKM],
        ]
    elif id == BNSTART:
        return [
            [Cmds.SetDirection, Constants.Direction_BN],
            [Cmds.WaitMsg, Constants.Msg_BNArrive],
            [Cmds.StartEmit, Constants.Msg_BNDepart],
            [Cmds.FastTrain],
            [Cmds.AddBatch, HITOKM],
        ]

    print("Unknown batch", id)
    return []
