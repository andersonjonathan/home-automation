# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-30 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radio', '0002_device_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='button',
            name='color',
            field=models.CharField(choices=[('default', 'White'), ('primary', 'Blue'), ('success', 'Green'), ('info', 'Light blue'), ('warning', 'Orange'), ('danger', 'Red')], default='default', max_length=255),
        ),
    ]