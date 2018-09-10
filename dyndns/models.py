from django.db import models


class LoopiaConfig(models.Model):
    username = models.CharField(max_length=511)
    password = models.CharField(max_length=511)
    type = models.CharField(max_length=511, choices=(('A', 'A'), ('AAAA', 'AAAA')))
    domain = models.CharField(max_length=511)
    subdomain = models.CharField(max_length=511, default="@")
    ttl = models.IntegerField(default=300)

    def __str__(self):
        if self.subdomain == '@':
            return '{}'.format(self.domain)
        else:
            return '{subdomain}.{domain}'.format(
                subdomain=self.subdomain,
                domain=self.domain)
