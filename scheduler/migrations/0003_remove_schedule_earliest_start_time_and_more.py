# Generated by Django 5.0.6 on 2024-08-07 06:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_remove_schedule_timerange_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='earliest_start_time',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='latest_end_time',
        ),
        migrations.AlterField(
            model_name='timerangeunion',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scheduler.schedule'),
        ),
    ]