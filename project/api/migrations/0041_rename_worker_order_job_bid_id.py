# Generated by Django 4.0.3 on 2023-09-21 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_alter_order_order_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='worker',
            new_name='job_bid_id',
        ),
    ]
