from django.core.management.base import BaseCommand
from tradfri.models import Gateway, TradfriLight


class Command(BaseCommand):
    help = 'Checks schedule and performs internal action.'

    def handle(self, *args, **options):
        gateways = Gateway.objects.all()
        for gateway in gateways:
            api = gateway.get_api()
            lights = Gateway.get_lights(api)
            db_lights = list(gateway.lights.all())
            lights_ids = [d.id for d in lights]
            db_lights_ids = [d.light_id for d in db_lights]
            for light in lights:
                if light.id not in db_lights_ids:
                    TradfriLight.objects.create(light_id=light.id, name=light.name, gateway=gateway)
            for light in db_lights:
                if light.light_id not in lights_ids:
                    light.delete()
