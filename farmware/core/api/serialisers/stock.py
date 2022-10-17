from django.conf import settings
from rest_framework import serializers
from ..models.stock import Stock, StockPickers

class StockSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class StockPickersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = StockPickers
        fields = '__all__'