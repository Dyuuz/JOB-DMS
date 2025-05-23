# Generated by Django 5.1.6 on 2025-04-11 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0016_remove_companyprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='work_mode',
            field=models.TextField(blank=True, choices=[('Remote', 'Remote'), ('Hybrid', 'Hybrid'), ('On site', 'On Site')], null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='highest_education_level',
            field=models.CharField(blank=True, choices=[('High School', 'High School'), ("Bachelor's Degree", "Bachelor's Degree"), ("Master's Degree", "Master's Degree"), ('PhD', 'PhD')], max_length=20),
        ),
    ]
