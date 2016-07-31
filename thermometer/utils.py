try:
    import Adafruit_DHT as Adafruit_DHT
except ImportError:
    from common.RPiMock import Adafruit_DHT


def read_retry(pin):
    return Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
