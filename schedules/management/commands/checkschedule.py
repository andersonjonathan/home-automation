from django.core.management.base import BaseCommand
from schedules.models import Schedule


class Command(BaseCommand):
    help = 'Checks schedule and performs internal action.'

    def handle(self, *args, **options):
        schedules = Schedule.objects.filter(active=True)
        for schedule in schedules:
            schedule.check_schedule()
