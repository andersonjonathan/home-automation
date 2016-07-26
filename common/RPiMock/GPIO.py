OUT = "OUT"
BCM = "BCM"


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


