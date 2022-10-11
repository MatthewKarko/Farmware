from django.conf import settings
from rest_framework import serializers
from ..models.order import Order
from ..models.order import OrderStock

class OrderSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderStockSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderStock
        fields = '__all__'