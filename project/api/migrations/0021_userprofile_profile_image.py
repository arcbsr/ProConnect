# Generated by Django 4.0.3 on 2023-08-25 20:28

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_userprofile_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]