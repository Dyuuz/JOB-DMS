# Generated by Django 5.1.6 on 2025-06-19 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0051_application_current_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='profile_viewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='application',
            name='resume_viewed',
            field=models.BooleanField(default=False),
        ),
    ]
