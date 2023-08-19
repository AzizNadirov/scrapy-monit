# Generated by Django 4.2.4 on 2023-08-19 11:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_initial'),
        ('schedules', '0003_triggeroncemodel_name_triggerperiodicmodel_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='spider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedules', to='monitor.spidermodel', to_field='identifier'),
        ),
        migrations.AlterField(
            model_name='triggeroncemodel',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 19, 23, 8, 8, 686048), verbose_name='Start time'),
        ),
        migrations.AlterField(
            model_name='triggerperiodicmodel',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 19, 11, 8, 8, 686346), verbose_name='Start time'),
        ),
    ]