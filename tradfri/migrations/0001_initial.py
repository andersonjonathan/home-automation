# Generated by Django 2.0.1 on 2018-02-19 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0003_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('function', models.CharField(choices=[('set_state', 'state'), ('set_dimmer', 'dimmer'), ('set_color', 'color')], default='state', help_text='Allowed values state=[0:1], dimmer=[1:254], color=[250:454]', max_length=255)),
                ('action_value', models.IntegerField(default=1)),
                ('current_value', models.IntegerField(default=1)),
                ('action', models.CharField(choices=[('add', 'add'), ('subtract', 'subtract'), ('fixed', 'fixed')], default='state', max_length=255)),
                ('color', models.CharField(choices=[('default', 'White'), ('primary', 'Blue'), ('success', 'Green'), ('info', 'Light blue'), ('warning', 'Orange'), ('danger', 'Red')], default='default', max_length=255)),
                ('priority', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('manually_active', models.BooleanField(default=False)),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='tradfri', serialize=False, to='common.BaseButton')),
            ],
            options={
                'ordering': ['priority'],
            },
            bases=('common.basebutton',),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('hide_schedule', models.BooleanField(default=False)),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='tradfri', serialize=False, to='common.BaseDevice')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tradfri', to='common.Room')),
            ],
            bases=('common.basedevice',),
        ),
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=15)),
                ('key', models.CharField(max_length=16)),
                ('identity', models.CharField(max_length=255)),
                ('psk', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TradfriLight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('light_id', models.IntegerField()),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='light', to='tradfri.Gateway')),
            ],
        ),
        migrations.AddField(
            model_name='button',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buttons', to='tradfri.Device'),
        ),
        migrations.AddField(
            model_name='button',
            name='gateway',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buttons', to='tradfri.Gateway'),
        ),
        migrations.AddField(
            model_name='button',
            name='lights',
            field=models.ManyToManyField(to='tradfri.TradfriLight'),
        ),
        migrations.AlterUniqueTogether(
            name='button',
            unique_together={('name', 'device')},
        ),
    ]