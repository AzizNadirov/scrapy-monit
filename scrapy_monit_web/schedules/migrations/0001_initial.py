# Generated by Django 4.2.4 on 2023-08-12 12:26

import datetime
from django.db import migrations, models
import django.db.models.deletion
import monitor.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('monitor', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
        ),
        migrations.CreateModel(
            name='TriggerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Trigger')),
                ('object_id', models.PositiveIntegerField()),
                ('status', models.BooleanField(default=True, verbose_name='Active')),
            ],
        ),
        migrations.CreateModel(
            name='TriggerOnceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField(default=datetime.datetime(2023, 8, 13, 0, 26, 31, 370928), verbose_name='Start time')),
                ('del_end', models.BooleanField(default=True, verbose_name='Delete at the End')),
            ],
        ),
        migrations.CreateModel(
            name='TriggerPeriodicModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField(default=datetime.datetime(2023, 8, 12, 12, 26, 31, 371280), verbose_name='Start time')),
                ('cron_str', models.CharField(max_length=60, validators=[monitor.validators.validate_cron_string], verbose_name='Cron Pattern')),
            ],
        ),
        migrations.CreateModel(
            name='TriggerSequenceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('use_spider_start', models.BooleanField(default=True, verbose_name='Use Spider Start')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('detanator_spider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='binded_seq_triggers', to='monitor.spidermodel')),
                ('spiders', models.ManyToManyField(related_name='seq_triggers', to='monitor.spidermodel', verbose_name='Spiders')),
            ],
        ),
    ]
