from pybricks.tools import wait


def ramp_power(motor, fromPower, toPower, ms=250):
    motor.dc(toPower)
    # p = fromPower;
    # if p == 0:
    #     p = 10;

    # mult = 10;
    # if fromPower > toPower:
    #     mult = -10;
    # while (fromPower > toPower and p > toPower) or (fromPower < toPower and p < toPower):
    #     p = p + mult;
    #     motor.dc(p);
    #     wait(ms);

    return
