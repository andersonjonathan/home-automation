from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_auto_20180203_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
