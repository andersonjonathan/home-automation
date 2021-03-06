# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-01 19:28


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CapacitorDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('gpio', models.IntegerField(help_text='GPIO port', unique=True)),
                ('a', models.FloatField(help_text='y=a*ln(x)+b')),
                ('b', models.FloatField(help_text='y=a*ln(x)+b')),
            ],
        ),
    ]
