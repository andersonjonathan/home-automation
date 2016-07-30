from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from common.models import BaseDevice, BaseButton
from schedules.sun import sun


class Schedule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    device = models.ManyToManyField(BaseDevice)
    on = models.ManyToManyField(BaseButton, related_name="schedule_on")
    off = models.ManyToManyField(BaseButton, related_name="schedule_off")

    def __unicode__(self):
        return u'{name}'.format(name=self.name)

    def active_slot(self):
        slots = self.scheduleslot_set.all()
        now = timezone.datetime.now().time()
        for slot in slots:
            if slot.start_time <= now <= slot.end_time:
                return slot
        return None


class ScheduleSlot(models.Model):
    TIME = 't'
    SUN_UP = 'u'
    SUN_DOWN = 'd'
    MODES = (
        (TIME, 'Time'),
        (SUN_UP, 'Sun up'),
        (SUN_DOWN, 'Sun down'),
    )
    start_mode = models.CharField(max_length=1,
                                  choices=MODES,
                                  default=TIME)

    start = models.TimeField(null=True, blank=True)

    end_mode = models.CharField(max_length=1,
                                choices=MODES,
                                default=TIME)

    end = models.TimeField(null=True, blank=True)
    schedule = models.ForeignKey(Schedule)

    @property
    def start_time(self):
        if self.start_mode == self.TIME:
            return self.start
        elif self.start_mode == self.SUN_UP:
            return sun(58.41, 15.57).sunrise()
        elif self.start_mode == self.SUN_DOWN:
            return sun(58.41, 15.57).sunset()

    @property
    def end_time(self):
        if self.end_mode == self.TIME:
            return self.end
        elif self.end_mode == self.SUN_UP:
            return sun(58.41, 15.57).sunrise()
        elif self.end_mode == self.SUN_DOWN:
            return sun(58.41, 15.57).sunset()

    def __unicode__(self):
        return u'{start} ({start_style}) - {end} ({end_style})'.format(
            start=self.start_time, end=self.end_time,
            start_style=self.get_start_mode_display(), end_style=self.get_end_mode_display())
