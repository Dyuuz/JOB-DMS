# Generated by Django 5.1.6 on 2025-06-18 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0048_userprofile_work_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employment',
            name='end_date',
            field=models.DateField(blank=True),
        ),
    ]
