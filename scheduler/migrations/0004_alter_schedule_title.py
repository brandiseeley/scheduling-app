# Generated by Django 5.0.6 on 2024-08-14 07:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_remove_schedule_earliest_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='title',
            field=models.CharField(max_length=300, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
    ]