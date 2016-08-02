try:
    import Adafruit_DHT as Adafruit_DHT
except ImportError:
    from common.RPiMock import Adafruit_DHT
try:
    import RPi.GPIO as GPIO
except ImportError:
    from common.RPiMock import GPIO

import os
import glob
import time
import math


def read_retry(pin):
    return Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)


def _RCtime_no_sleep(RCpin):
    GPIO.setmode(GPIO.BCM)
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(RCpin, GPIO.IN)
    while GPIO.input(RCpin) == GPIO.LOW:
        reading += 1
    return reading


def read_capacitor_raw(pin):
    temps = []
    i = 0
    while True:
        temps.append(_RCtime(pin))
        i += 1
        if i >= 19:
            return max(temps)


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


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


def w1_read_temp_raw():
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def w1_read_temp():
    lines = w1_read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = w1_read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
