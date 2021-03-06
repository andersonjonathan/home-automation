# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-28 19:26


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('payload', models.CharField(choices=[(b'0', b'0'), (b'1', b'1')], max_length=1)),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(choices=[(b'btn-default', b'White'), (b'btn-primary', b'Blue'), (b'btn-success', b'Green'), (b'btn-info', b'Light blue'), (b'btn-warning', b'Orange'), (b'btn-danger', b'Red')], default=b'btn-default', max_length=255)),
                ('priority', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='wired', serialize=False, to='common.BaseButton')),
            ],
            bases=('common.basebutton',),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('gpio', models.IntegerField(help_text=b'GPIO port', unique=True)),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='wired', serialize=False, to='common.BaseDevice')),
            ],
            bases=('common.basedevice',),
        ),
        migrations.AddField(
            model_name='button',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buttons', to='wired.Device'),
        ),
    ]
