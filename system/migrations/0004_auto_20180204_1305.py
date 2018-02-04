# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-04 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_button_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='manually_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='hide_schedule',
            field=models.BooleanField(default=False),
        ),
    ]
