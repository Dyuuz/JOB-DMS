# Generated by Django 5.1.6 on 2025-06-30 07:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0074_teammanagement_unique_user_job_team_management'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammanagement',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
