from django.core.management.base import BaseCommand
from schedules.models import Schedule


class Command(BaseCommand):
    help = 'Checks schedule and performs internal action.'

    def handle(self, *args, **options):
        schedules = Schedule.objects.filter(active=True)
        for schedule in schedules:
            slot = schedule.active_slot()
            if slot:
                for btn in schedule.on.all():
                    btn.child.perform_action_internal()
            else:
                for btn in schedule.off.all():
                    btn.child.perform_action_internal()
