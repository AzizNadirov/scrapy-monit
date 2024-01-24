# Generated by Django 5.0.1 on 2024-01-24 12:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('monitor', '0002_initial'),
        ('schedules', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='spider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedules', to='monitor.spidermodel', to_field='identifier'),
        ),
        migrations.AddField(
            model_name='triggermodel',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='triggers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='triggermodel',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='trigger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule', to='schedules.triggermodel'),
        ),
        migrations.AddField(
            model_name='triggersequencemodel',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='triggersequencemodel',
            name='detanator_spider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='binded_seq_triggers', to='monitor.spidermodel'),
        ),
        migrations.AddField(
            model_name='triggersequencemodel',
            name='spiders',
            field=models.ManyToManyField(related_name='seq_triggers', to='monitor.spidermodel', verbose_name='Spiders'),
        ),
    ]