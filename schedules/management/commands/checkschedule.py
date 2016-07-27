from django.core.management.base import BaseCommand
# from wired.models import


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # plugs = Plug.objects.filter(in_auto_mode=True)
        #
        # for plug in plugs:
        #     if hasattr(plug, 'radioplug'):
        #         plug = plug.radioplug
        #     if hasattr(plug, 'wiredplug'):
        #         plug = plug.wiredplug
        #     slot = plug.schedule.active_slot()
        #     if slot:
        #         slot.button.child().perform_action_internal()
        #     else:
        #         plug.default_button.child().perform_action_internal()
        pass
