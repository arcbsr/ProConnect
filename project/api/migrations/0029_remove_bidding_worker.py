# Generated by Django 4.0.3 on 2023-08-29 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_remove_bidding_job_poster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidding',
            name='worker',
        ),
    ]