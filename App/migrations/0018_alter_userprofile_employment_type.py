# Generated by Django 5.1.6 on 2025-04-11 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0017_alter_companyprofile_work_mode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='employment_type',
            field=models.CharField(blank=True, choices=[('Internship', 'Internship'), ('Part Time', 'Part Time'), ('Full Time', 'Full Time'), ('Contract', 'Contract')], max_length=20),
        ),
    ]
