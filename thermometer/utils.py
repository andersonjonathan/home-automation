try:
    import Adafruit_DHT as Adafruit_DHT
except ImportError:
    from common.RPiMock import Adafruit_DHT
try:
    import RPi.GPIO as GPIO
except ImportError:
    from common.RPiMock import GPIO

import time
import math


def read_retry(pin):
    return Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)


def _RCtime(RCpin):
    GPIO.setmode(GPIO.BCM)
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(RCpin, GPIO.IN)
    while GPIO.input(RCpin) == GPIO.LOW:
        time.sleep(0.0001)
        reading += 1
    return reading


def read_capacitor(pin, a, b):
    temps = []
    i = 0
    while True:
        temps.append(_RCtime(pin))
        i += 1
        if i >= 9:
            return a*math.log(max(temps))+b
