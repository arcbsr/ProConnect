# Generated by Django 4.0.3 on 2023-08-25 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_jobdescription_keyword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdescription',
            name='description',
            field=models.TextField(null=True),
        ),
    ]