# Generated by Django 2.2.4 on 2019-08-15 22:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('connexion', '0015_auto_20190815_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='date_upload',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 15, 22, 26, 12, 338092, tzinfo=utc)),
        ),
    ]