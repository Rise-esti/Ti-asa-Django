# Generated by Django 2.2.4 on 2019-08-15 17:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('connexion', '0014_auto_20190815_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='mission',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='competence',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='date_upload',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 15, 17, 4, 24, 373909, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='publication',
            name='experience',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='formation',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='langue',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='lieu',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='personnalite',
            field=models.TextField(null=True),
        ),
    ]
