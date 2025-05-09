# Generated by Django 5.1.6 on 2025-04-05 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_rename_company_name_companyprofile_company_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='DOB',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='certifications',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='highest_education_level',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='occupation',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='skills',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='street_address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='years_of_experience',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='industry',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(max_length=255),
        ),
    ]
