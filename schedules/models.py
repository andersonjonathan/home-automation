from __future__ import unicode_literals

from datetime import time, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from common.models import BaseDevice, BaseButton
from schedules.sun import sun


class Schedule(models.Model):
    device = models.ForeignKey(BaseDevice, related_name="schedule", null=True, blank=False)
    active = models.BooleanField(default=True)
    on = models.ForeignKey(BaseButton, related_name="schedule_on", null=True, blank=True)
    off = models.ForeignKey(BaseButton, related_name="schedule_off", null=True, blank=True)
    repeat_signal = models.BooleanField(default=False)
    disable_until = models.DateTimeField(null=True, blank=True)
    last_action = models.BooleanField(default=True)  # True = on, False = off

    def __unicode__(self):
        return unicode(self.device)

    def get_state(self, now=None):
        if not now:
            now = timezone.datetime.now()
        weekday = now.weekday()
        weekday_map = {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday',
        }
        slots = sorted(self.scheduleslot_set.filter(**{
            weekday_map[weekday]: True
        }), key=lambda t: t.start_time)
        now_time = now.time()
        off_start = time(0, 0, 0)
        off_end = None
        for slot in slots:
            if slot.start_time <= now_time <= slot.end_time:
                timezone.datetime.combine(now.date(), slot.start_time)
                return {
                    'state': 'on',
                    'start': timezone.datetime.combine(now.date(), slot.start_time),
                    'end': timezone.datetime.combine(now.date(), slot.end_time),
                }
            elif now_time > slot.end_time:
                off_start = slot.end_time
            elif now_time < slot.start_time and not off_end:
                off_end = timezone.datetime.combine(now.date(), slot.start_time)
        if not off_end:
            tomorrows_slots = sorted(self.scheduleslot_set.filter(**{
                weekday_map[(weekday + 1) % 7]: True
            }), key=lambda t: t.start_time)
            if tomorrows_slots:
                off_end = timezone.datetime.combine(now.date()+timedelta(days=1), tomorrows_slots[0].start_time)
            else:
                off_end = timezone.datetime.combine(now.date(), time(23, 59, 59))
        return {
            'state': 'off',
            'start': timezone.datetime.combine(now.date(), off_start),
            'end': off_end,
        }

    def _turn_on(self):
        self.last_action = True
        self.save()
        if self.on:
            self.on.child.perform_action_internal()

    def _turn_off(self):
        self.last_action = False
        self.save()
        if self.off:
            self.off.child.perform_action_internal()

    def check_schedule(self):
        if not self.active:
            return
        if self.disable_until:
            if timezone.now() < self.disable_until:
                return
            else:
                self.disable_until = None
                self.save()
        slot = self.get_state()
        if slot['state'] == 'on' and (self.repeat_signal or (not self.last_action)):
            self._turn_on()
        elif self.repeat_signal or self.last_action:
            self._turn_off()


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

    start = models.FloatField(
        default=0,
        validators=[MinValueValidator(-23.99), MaxValueValidator(23.99)],
        help_text="Time between 00:00 and 23:59, expressed as decimal numbers ex: 12:15 = 12.25. May be negative if start mode is not set to time to add an offset."
    )

    end_mode = models.CharField(max_length=1,
                                choices=MODES,
                                default=TIME)

    end = models.FloatField(
        default=0,
        validators=[MinValueValidator(-23.99), MaxValueValidator(23.99)],
        help_text = "Time between 00:00 and 23:59, expressed as decimal numbers ex: 12:15 = 12.25. May be negative if start mode is not set to time to add an offset."
    )

    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=True)

    schedule = models.ForeignKey(Schedule)

    @property
    def start_time(self):
        if self.start_mode == self.TIME:
            return time(int(abs(self.start)), int((abs(self.start)-int(abs(self.start)))*60))
        elif self.start_mode == self.SUN_UP:
            sunrise = sun(58.41, 15.57).sunrise()
            hour = max(0.0, min(sunrise.hour + (sunrise.minute / 60.0) + self.start, 23.99))
            return time(int(hour), int((hour - int(hour)) * 60))
        elif self.start_mode == self.SUN_DOWN:
            sunset = sun(58.41, 15.57).sunset()
            hour = max(0.0, min(sunset.hour + (sunset.minute / 60.0) + self.start, 23.99))
            return time(int(hour), int((hour - int(hour)) * 60))

    @property
    def end_time(self):
        if self.end_mode == self.TIME:
            return time(int(abs(self.end)), int((abs(self.end)-int(abs(self.end)))*60))
        elif self.end_mode == self.SUN_UP:
            sunrise = sun(58.41, 15.57).sunrise()
            hour = max(0.0, min(sunrise.hour + (sunrise.minute / 60.0) + self.end, 23.99))
            return time(int(hour), int((hour - int(hour)) * 60))
        elif self.end_mode == self.SUN_DOWN:
            sunset = sun(58.41, 15.57).sunset()
            hour = max(0.0, min(sunset.hour + (sunset.minute / 60.0) + self.end, 23.99))
            return time(int(hour), int((hour - int(hour)) * 60))

    @property
    def days(self):
        days = ''
        if self.monday:
            days += 'Mo, '
        if self.tuesday:
            days += 'Tu, '
        if self.wednesday:
            days += 'We, '
        if self.thursday:
            days += 'Th, '
        if self.friday:
            days += 'Fr, '
        if self.saturday:
            days += 'Sa, '
        if self.sunday:
            days += 'Su, '
        if days:
            days = days[:-2]
        return days

    @property
    def times(self):
        return '{start} - {end}'.format(
            start=self.start_time, end=self.end_time,
        )

    @property
    def current_setting(self):
        start_setting = None
        end_setting = None
        if self.end_mode != self.TIME:
            end_setting = '{} {}{:}:{:02d}'.format(
                self.get_end_mode_display(),
                ('+', '-')[self.end < 0],
                int(abs(self.end)),
                int((abs(self.end) - int(abs(self.end))) * 60),
            )
        else:
            end_setting = self.end_time
        if self.start_mode != self.TIME:
            start_setting = '{} {}{}:{:02d}'.format(
                self.get_start_mode_display(),
                ('+', '-')[self.start < 0],
                int(abs(self.start)),
                int((abs(self.start) - int(abs(self.start))) * 60)
            )
        else:
            start_setting = self.start_time

        return '({start}) - ({end})'.format(
            start=start_setting, end=end_setting
        )

    def __unicode__(self):
        return '{settings}, [{days}], '.format(
            settings=self.current_setting,
            days=self.days,
        )
