# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-14 11:13


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20180102_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='button',
            name='content_type',
            field=models.CharField(blank=True, default='application/json', max_length=255, null=True),
        ),
    ]
