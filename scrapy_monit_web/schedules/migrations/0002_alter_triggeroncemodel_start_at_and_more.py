# Generated by Django 4.2.4 on 2023-08-15 17:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triggeroncemodel',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 16, 5, 38, 46, 175320), verbose_name='Start time'),
        ),
        migrations.AlterField(
            model_name='triggerperiodicmodel',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 17, 38, 46, 175586), verbose_name='Start time'),
        ),
    ]
