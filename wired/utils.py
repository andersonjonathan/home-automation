try:
    import RPi.GPIO as GPIO
except ImportError:
    from common import RPiMock as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def set_state(gpio, action):
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, action)
