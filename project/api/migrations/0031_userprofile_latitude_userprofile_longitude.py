# Generated by Django 4.0.3 on 2023-08-30 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_bidding_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
