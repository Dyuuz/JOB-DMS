# Generated by Django 5.1.6 on 2025-06-26 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0062_alter_job_experience_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='about',
            field=models.TextField(blank=True),
        ),
    ]
