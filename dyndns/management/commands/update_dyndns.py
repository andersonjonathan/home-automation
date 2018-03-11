import xmlrpc.client
import urllib.request
import re
from django.core.management.base import BaseCommand
from dyndns.models import LoopiaConfig


class Command(BaseCommand):
    help = 'Checks schedule and performs internal action.'

    def handle(self, *args, **options):
        configs = LoopiaConfig.objects.all()
        for config in configs:
            client = xmlrpc.client.ServerProxy(
                uri='https://api.loopia.se/RPCSERV',
                encoding='utf-8')

            a_records = get_records(client, config)
            new_ip = get_ip()

            if len(a_records) == 0:
                status = '{status}. Added new record.'.format(
                        status=add_record(client, config, new_ip))
            elif a_records[0]['rdata'] != new_ip:
                status = update_record(client, config, new_ip, a_records[0])
            else:
                status = "No change"

            if config.subdomain == '@':
                res = '{domain}: {status}'.format(
                    domain=config.domain,
                    status=status)
            else:
                res = '{subdomain}.{domain}: {status}'.format(
                    subdomain=config.subdomain,
                    domain=config.domain,
                    status=status)

            print("ip: {}; {}".format(new_ip, res))


def get_ip():
    """Get public IP adress"""
    result = urllib.request.urlopen('http://dyndns.loopia.se/checkip').read()
    return re.search('[0-9.]+', str(result)).group(0)


def get_records(client, config):
    """Get current zone records"""
    zone_records = client.getZoneRecords(
        config.username,
        config.password,
        config.domain,
        config.subdomain)
    return [d for d in zone_records if d['type'] == 'A']


def add_record(client, config, ip):
    """Add a new A record if we don't have any"""
    return client.addZoneRecord(
        config.username,
        config.password,
        config.domain,
        config.subdomain,
        {
            'priority': '',
            'rdata': ip,
            'type': 'A',
            'ttl': config.ttl
        })


def update_record(client, config, ip, record):
    """Update current A record"""
    return client.updateZoneRecord(
        config.username,
        config.password,
        config.domain,
        config.subdomain,
        {
            'priority': record['priority'],
            'record_id': record['record_id'],
            'rdata': ip,
            'type': record['type'],
            'ttl': record['ttl']
        })
