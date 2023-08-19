# Generated by Django 4.2.4 on 2023-08-15 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('monitor', '0001_initial'),
        ('schedules', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='spidermodel',
            name='triggers',
            field=models.ManyToManyField(null=True, related_name='spiders', to='schedules.triggermodel'),
        ),
        migrations.AddField(
            model_name='projectmodel',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='monitor.instancemodel'),
        ),
        migrations.AddField(
            model_name='jobmodel',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='monitor.instancemodel', verbose_name='instance'),
        ),
        migrations.AddField(
            model_name='jobmodel',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='monitor.projectmodel', verbose_name='project'),
        ),
        migrations.AddField(
            model_name='jobmodel',
            name='spider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='monitor.spidermodel', verbose_name='spider'),
        ),
        migrations.AddField(
            model_name='instancemodel',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]