from django.db import models
from api.models.JobBidding import Bidding
from rest_framework import serializers
import uuid

import secrets
import string



def generate_unique_string(length=32):
    # Define characters to use for the string
    characters = string.ascii_letters + string.digits

    # Generate a random string of the specified length
    unique_string = ''.join(secrets.choice(characters) for _ in range(length))

    return unique_string


class Order(models.Model):
    job_bid = models.ForeignKey(Bidding, on_delete=models.CASCADE, null=True,blank=True)
    order_number = models.CharField(
        max_length=32,  # Set the desired length for your unique string
        default=uuid.uuid4().hex,  # Generate a random unique string
        unique=True,  # Ensure uniqueness in the database
        editable=False  # Prevent manual editing in the Django admin
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(null=True,blank=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

