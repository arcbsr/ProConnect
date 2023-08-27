from versatileimagefield.fields import VersatileImageField, PPOIField
from django.db import models
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

class Image(models.Model):
    name = models.CharField(max_length=255)
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    def __str__(self):
        return self.name
    


class ImageSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
        ]
    )

    class Meta:
        model = Image
        fields = ['pk', 'name', 'image']