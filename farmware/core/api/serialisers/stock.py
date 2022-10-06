from django.conf import settings
from rest_framework import serializers
from ..models.stock import Stock, StockPickers

class StockSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['produce_id', 'variety_id', 'quantity', 'quantity_suffix_id', 'supplier_id', 'date_seeded', 'date_planted', 'date_picked', 'ehd', 'date_completed', 'area_code']

class StockPickersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = StockPickers
        fields = ['stock_id', 'user_id']