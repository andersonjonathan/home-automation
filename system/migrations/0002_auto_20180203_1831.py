from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_url'),
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='system', to='common.Room'),
        ),
        migrations.AlterField(
            model_name='button',
            name='color',
            field=models.CharField(choices=[('default', 'White'), ('primary', 'Blue'), ('success', 'Green'), ('info', 'Light blue'), ('warning', 'Orange'), ('danger', 'Red')], default='default', max_length=255),
        ),
    ]
