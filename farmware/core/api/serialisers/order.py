from django.conf import settings
from rest_framework import serializers
from ..models.order import Order
from ..models.order import OrderStock

class OrderSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer_id']

class OrderStockSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderStock
        fields = ['order_id', 'stock_id', 'quantity', 'quantity_suffix_id', 'invoice_number']