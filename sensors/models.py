from __future__ import unicode_literals
import requests
from django.db import models
from utils import read_retry, read_capacitor, w1_read_temp, read_capacitor_raw, read_mcp, thermistor_table_lookup


class Reading(models.Model):
    identity = models.CharField(max_length=254)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __unicode__(self):
        return '{name} {ts}'.format(name=self.identity, ts=self.timestamp)


class DHT11(models.Model):
    name = models.CharField(max_length=254)
    gpio = models.IntegerField(help_text="GPIO port", unique=True)
    last_temperature = models.IntegerField(null=True, blank=True)
    last_humidity = models.IntegerField(null=True, blank=True)
    save_temperature = models.BooleanField(default=False)
    save_humidity = models.BooleanField(default=False)
    show_temperature = models.BooleanField(default=False)
    show_humidity = models.BooleanField(default=False)

    @property
    def temperature(self):
        return self.read_retry[1]

    @property
    def humidity(self):
        return self.read_retry[0]

    @property
    def read_retry(self):
        return read_retry(self.gpio)

    def __unicode__(self):
        return '{name}'.format(name=self.name)


class CapacitorDevice(models.Model):
    name = models.CharField(max_length=254)
    gpio = models.IntegerField(help_text="GPIO port", unique=True)
    a = models.FloatField(help_text="y=a*ln(x)+b")
    b = models.FloatField(help_text="y=a*ln(x)+b")
    unit = models.CharField(max_length=254, null=True, blank=True)
    last_value = models.FloatField(null=True, blank=True)
    save_value = models.BooleanField(default=False)

    @property
    def value(self):
        if self.a == 0 and self.b == 0:
            return self.value_raw
        return read_capacitor(self.gpio, self.a, self.b)

    @property
    def value_raw(self):
        return read_capacitor_raw(self.gpio)

    def __unicode__(self):
        return '{name}'.format(name=self.name)


class W1Therm(models.Model):
    name = models.CharField(max_length=254)
    unit = models.CharField(max_length=254, null=True, blank=True)
    save_temperature = models.BooleanField(default=False)

    @property
    def temperature(self):
        return w1_read_temp()


class MCP3008(models.Model):
    name = models.CharField(max_length=254)
    clk = models.IntegerField(help_text="CLK")
    miso = models.IntegerField(help_text="MISO")
    mosi = models.IntegerField(help_text="MOSI")
    cs = models.IntegerField(help_text="CS")

    def __unicode__(self):
        return '{name}'.format(name=self.name)


class MCP3008Channel(models.Model):
    THERMISTOR = 't'
    VALUE = 'v'
    PERCENT = 'p'
    RESISTANCE = 'r'
    MODES = (
        (THERMISTOR, 'Thermistor'),
        (VALUE, 'Value'),
        (PERCENT, 'Percent'),
        (RESISTANCE, "Resistance")
    )
    name = models.CharField(max_length=254)
    type = models.CharField(max_length=1,
                            choices=MODES,
                            default=VALUE)
    unit = models.CharField(max_length=254, null=True, blank=True)
    MCP3008 = models.ForeignKey(MCP3008)
    channel = models.IntegerField(help_text="Channel")
    decimals = models.IntegerField(default=2, help_text="Number of decimals to show")
    series_resistor = models.FloatField(default=10.0, null=True, blank=True, help_text="Resistor value in kohm, must be set on Thermistor and Resistance")
    save_value = models.BooleanField(default=False)

    @property
    def value(self):
        raw_value = read_mcp(self.MCP3008.clk, self.MCP3008.miso, self.MCP3008.mosi, self.MCP3008.cs, self.channel)
        if self.type == MCP3008Channel.THERMISTOR:
            resistance = self.series_resistor / (1023.0 / raw_value - 1.0)
            return thermistor_table_lookup(resistance)
        if self.type == MCP3008Channel.VALUE:
            return raw_value
        if self.type == MCP3008Channel.PERCENT:
            return (raw_value/1023.0) * 100
        if self.type == MCP3008Channel.RESISTANCE:
            return self.series_resistor / (1023.0 / raw_value - 1.0)

    @property
    def formatted_value(self):
        return '{:.{prec}f}{unit}'.format(self.value, prec=self.decimals, unit=self.unit)

    def __unicode__(self):
        return '{name}'.format(name=self.name)


class NetworkSensor(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=511)
    post_body = models.TextField(blank=True, null=True)
    content_type = models.CharField(default="application/json", max_length=255, blank=True, null=True)
    method = models.CharField(max_length=10, choices=(
        ("post", "POST"),
        ("get", "GET"),))
    user = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    decimals = models.IntegerField(default=2, help_text="Number of decimals to show")
    unit = models.CharField(max_length=254, null=True, blank=True)
    response_parameter = models.CharField(max_length=254, null=True, blank=True)

    @property
    def value(self):
        if self.method == 'post':
            auth = None
            headers = {
                'cache-control': "no-cache",
            }
            if self.user:
                auth = (self.user, self.password)
            if self.content_type:
                headers['content-type'] = self.content_type
            res = requests.post(
                self.url,
                data=self.post_body,
                headers=headers,
                auth=auth
            )
            if self.response_parameter:
                return res.json()[self.response_parameter]
            else:
                return res.text
        elif self.method == 'get':
            auth = None
            if self.user:
                auth = (self.user, self.password)
            res = requests.get(
                self.url,
                headers={
                    'cache-control': "no-cache",
                },
                auth=auth
            )
            if self.response_parameter:
                return res.json()[self.response_parameter]
            else:
                return res.text

    @property
    def formatted_value(self):
        return '{:.{prec}f}{unit}'.format(self.value, prec=self.decimals, unit=self.unit)

    def __unicode__(self):
        return '{name}'.format(name=self.name)