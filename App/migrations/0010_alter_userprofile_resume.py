# Generated by Django 5.1.6 on 2025-04-09 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_alter_userprofile_highest_education_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
    ]
