try:
    import Adafruit_DHT as Adafruit_DHT
except ImportError:
    from common.RPiMock import Adafruit_DHT
try:
    import RPi.GPIO as GPIO
except ImportError:
    from common.RPiMock import GPIO
try:
    import Adafruit_MCP3008
except ImportError:
    from common.RPiMock import Adafruit_MCP3008
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


def read_mcp(clk, miso, mosi, cs, channel):
    mcp = Adafruit_MCP3008.MCP3008(clk=clk, cs=cs, miso=miso, mosi=mosi)
    return mcp.read_adc(channel)


def thermistor_table_lookup(resistance):
    # Resistance in kohm
    res_table = [
        [0.0619, 200.0], [0.0631, 199.0], [0.0645, 198.0], [0.0658, 197.0], [0.0672, 196.0], [0.0686, 195.0],
        [0.07, 194.0], [0.0714, 193.0], [0.0729, 192.0], [0.0743, 191.0], [0.0759, 190.0], [0.0774, 189.0],
        [0.079, 188.0], [0.0806, 187.0], [0.0822, 186.0], [0.0839, 185.0], [0.0856, 184.0], [0.0873, 183.0],
        [0.0891, 182.0], [0.0909, 181.0], [0.0928, 180.0], [0.0947, 179.0], [0.0966, 178.0], [0.0986, 177.0],
        [0.1006, 176.0], [0.1027, 175.0], [0.1048, 174.0], [0.107, 173.0], [0.1092, 172.0], [0.1115, 171.0],
        [0.1139, 170.0], [0.1163, 169.0], [0.1187, 168.0], [0.1213, 167.0], [0.1239, 166.0], [0.1265, 165.0],
        [0.1293, 164.0], [0.1321, 163.0], [0.135, 162.0], [0.1379, 161.0], [0.141, 160.0], [0.1441, 159.0],
        [0.1474, 158.0], [0.1507, 157.0], [0.1541, 156.0], [0.1576, 155.0], [0.1612, 154.0], [0.165, 153.0],
        [0.1688, 152.0], [0.1728, 151.0], [0.1769, 150.0], [0.1811, 149.0], [0.1855, 148.0], [0.19, 147.0],
        [0.1946, 146.0], [0.1994, 145.0], [0.2044, 144.0], [0.2095, 143.0], [0.2148, 142.0], [0.2202, 141.0],
        [0.2258, 140.0], [0.2316, 139.0], [0.2375, 138.0], [0.2437, 137.0], [0.25, 136.0], [0.2565, 135.0],
        [0.2633, 134.0], [0.2702, 133.0], [0.2774, 132.0], [0.2848, 131.0], [0.2924, 130.0], [0.3002, 129.0],
        [0.3083, 128.0], [0.3167, 127.0], [0.3253, 126.0], [0.3341, 125.0], [0.3434, 124.0], [0.353, 123.0],
        [0.3628, 122.0], [0.373, 121.0], [0.3835, 120.0], [0.3944, 119.0], [0.4055, 118.0], [0.4171, 117.0],
        [0.429, 116.0], [0.4412, 115.0], [0.4539, 114.0], [0.4669, 113.0], [0.4803, 112.0], [0.4941, 111.0],
        [0.5083, 110.0], [0.5229, 109.0], [0.538, 108.0], [0.5535, 107.0], [0.5694, 106.0], [0.5858, 105.0],
        [0.6026, 104.0], [0.6199, 103.0], [0.6376, 102.0], [0.6558, 101.0], [0.6744, 100.0], [0.6945, 99.0],
        [0.7152, 98.0], [0.7366, 97.0], [0.7587, 96.0], [0.7816, 95.0], [0.8052, 94.0], [0.8297, 93.0],
        [0.855, 92.0], [0.8812, 91.0], [0.9083, 90.0], [0.9363, 89.0], [0.9654, 88.0], [0.9955, 87.0],
        [1.027, 86.0], [1.059, 85.0], [1.093, 84.0], [1.128, 83.0], [1.165, 82.0], [1.203, 81.0],
        [1.243, 80.0], [1.284, 79.0], [1.326, 78.0], [1.371, 77.0], [1.417, 76.0], [1.465, 75.0],
        [1.515, 74.0], [1.567, 73.0], [1.621, 72.0], [1.677, 71.0], [1.735, 70.0], [1.796, 69.0], [1.86, 68.0],
        [1.926, 67.0], [1.994, 66.0], [2.066, 65.0], [2.141, 64.0], [2.218, 63.0], [2.299, 62.0],
        [2.384, 61.0], [2.472, 60.0], [2.564, 59.0], [2.659, 58.0], [2.759, 57.0], [2.863, 56.0],
        [2.972, 55.0], [3.086, 54.0], [3.204, 53.0], [3.328, 52.0], [3.457, 51.0], [3.592, 50.0],
        [3.733, 49.0], [3.88, 48.0], [4.034, 47.0], [4.195, 46.0], [4.363, 45.0], [4.539, 44.0], [4.723, 43.0],
        [4.915, 42.0], [5.117, 41.0], [5.327, 40.0], [5.548, 39.0], [5.778, 38.0], [6.02, 37.0], [6.273, 36.0],
        [6.538, 35.0], [6.815, 34.0], [7.106, 33.0], [7.41, 32.0], [7.73, 31.0], [8.064, 30.0], [8.416, 29.0],
        [8.784, 28.0], [9.17, 27.0], [9.575, 26.0], [10.0, 25.0], [10.45, 24.0], [10.91, 23.0], [11.41, 22.0],
        [11.92, 21.0], [12.47, 20.0], [13.04, 19.0], [13.63, 18.0], [14.26, 17.0], [14.93, 16.0],
        [15.62, 15.0], [16.35, 14.0], [17.12, 13.0], [17.93, 12.0], [18.78, 11.0], [19.68, 10.0], [20.63, 9.0],
        [21.62, 8.0], [22.67, 7.0], [23.77, 6.0], [24.94, 5.0], [26.16, 4.0], [27.45, 3.0], [28.82, 2.0],
        [30.25, 1.0], [31.77, 0.0], [33.33, -1.0], [34.97, -2.0], [36.7, -3.0], [38.53, -4.0], [40.45, -5.0],
        [42.48, -6.0], [44.62, -7.0], [46.89, -8.0], [49.28, -9.0], [51.82, -10.0], [54.5, -11.0],
        [57.33, -12.0], [60.34, -13.0], [63.54, -14.0], [66.92, -15.0], [70.53, -16.0], [74.36, -17.0],
        [78.44, -18.0], [82.79, -19.0], [87.43, -20.0], [92.5, -21.0], [97.9, -22.0], [103.7, -23.0],
        [110.0, -24.0], [116.6, -25.0], [123.7, -26.0], [131.3, -27.0], [139.4, -28.0], [148.1, -29.0],
        [157.2, -30.0], [167.0, -31.0], [177.3, -32.0], [188.1, -33.0], [199.6, -34.0], [211.5, -35.0],
        [224.0, -36.0], [236.8, -37.0], [250.1, -38.0], [263.6, -39.0], [277.2, -40.0]]

    last = None
    for p in res_table:
        if p[0] > resistance:
            if not last:
                return 200
            percent_p = (resistance - last[0]) / (p[0] - last[0])
            return percent_p * p[1] + (1 - percent_p) * last[1]
        else:
            last = p
    return -40