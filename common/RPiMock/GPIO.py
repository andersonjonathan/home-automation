import random
import math

OUT = "OUT"
BCM = "BCM"
IN = "IN"
LOW = 0
HIGH = 1


def setmode(mode):
    print("setmode", mode)
    return None


def setwarnings(warning):
    print("setwarnings", warning)
    return None


def setup(sender, mode):
    print("setup sender", sender)
    print("setup mode", mode)
    return None


def output(sender, param):
    print("output sender", sender)
    print("output param", param)
    return None


def input(RCpin):
    print("output sender", RCpin)
    return math.pow(random.randint(0, 1), 5)
