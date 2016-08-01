# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-31 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DHT11',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('gpio', models.IntegerField(help_text='GPIO port', unique=True)),
            ],
        ),
    ]