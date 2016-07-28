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
        status = None
        now = timezone.datetime.now().time()
        for slot in slots:
            slot_status = None
            if slot.start_mode == slot.TIME:
                if now >= slot.start:
                    slot_status = slot
            elif slot.start_mode == slot.SUN_UP:
                if now >= sun(58.41, 15.57).sunrise():
                    slot_status = slot
            elif slot.start_mode == slot.SUN_DOWN:
                if now >= sun(58.41, 15.57).sunset():
                    slot_status = slot
            if slot_status:
                if slot.end_mode == slot.TIME:
                    if now <= slot.end:
                        status = slot
                elif slot.end_mode == slot.SUN_UP:
                    if now <= sun(58.41, 15.57).sunrise():
                        status = slot
                elif slot.end_mode == slot.SUN_DOWN:
                    if now <= sun(58.41, 15.57).sunset():
                        status = slot
        return status


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

    def __unicode__(self):
        return u'{name}'.format(name=self.schedule.name)