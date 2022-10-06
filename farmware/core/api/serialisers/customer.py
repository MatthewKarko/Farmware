from django.conf import settings
from rest_framework import serializers
from ..models.customer import Customer

class CustomerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number']