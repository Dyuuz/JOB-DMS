# Generated by Django 5.1.6 on 2025-06-11 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0040_application_portfolio_alter_application_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='company',
        ),
        migrations.RemoveField(
            model_name='application',
            name='job_title',
        ),
    ]
