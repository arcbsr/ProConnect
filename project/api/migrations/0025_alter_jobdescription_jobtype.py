# Generated by Django 4.0.3 on 2023-08-27 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_type_jobdescription_jobtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdescription',
            name='jobtype',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='api.type'),
        ),
    ]
