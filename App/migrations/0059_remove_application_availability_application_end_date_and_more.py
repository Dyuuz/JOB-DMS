# Generated by Django 5.1.6 on 2025-06-24 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0058_alter_userprofile_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='availability',
        ),
        migrations.AddField(
            model_name='application',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='file_format',
            field=models.CharField(choices=[('pdf', 'pdf'), ('txt', 'txt'), ('docx', 'docx'), ('doc', 'doc')], default='pdf', max_length=50),
        ),
    ]
