# Generated by Django 2.2.4 on 2019-08-13 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connexion', '0002_auto_20190813_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='description',
            field=models.TextField(null=True),
        ),
    ]