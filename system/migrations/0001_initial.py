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
                ('call', models.CharField(max_length=1023)),
                ('color', models.CharField(choices=[('btn-default', 'White'), ('btn-primary', 'Blue'), ('btn-success', 'Green'), ('btn-info', 'Light blue'), ('btn-warning', 'Orange'), ('btn-danger', 'Red')], default='btn-default', max_length=255)),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='system', serialize=False, to='common.BaseButton')),
            ],
            bases=('common.basebutton',),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('name', models.CharField(max_length=255, unique=True)),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='system', serialize=False, to='common.BaseDevice')),
            ],
            bases=('common.basedevice',),
        ),
        migrations.AddField(
            model_name='button',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buttons', to='system.Device'),
        ),
    ]
