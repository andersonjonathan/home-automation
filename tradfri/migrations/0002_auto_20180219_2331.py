# Generated by Django 2.0.1 on 2018-02-19 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tradfri', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradfrilight',
            name='gateway',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lights', to='tradfri.Gateway'),
        ),
    ]