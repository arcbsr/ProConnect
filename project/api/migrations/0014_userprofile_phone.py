# Generated by Django 4.0.3 on 2023-08-25 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]