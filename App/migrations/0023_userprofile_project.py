# Generated by Django 5.1.6 on 2025-04-11 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0022_rename_country_userprofile_job_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='project',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
