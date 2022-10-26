from django.conf import settings
from rest_framework import serializers
from ..models.stock import Stock, StockPickers


### STOCK #####################################################################
class StockSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class BulkAddStockSerialiser(serializers.ModelSerializer):
    quantity = serializers.FloatField()
    class Meta:
        model = Stock
        fields = ['id', 'quantity']
###############################################################################


### STOCK PICKERS #############################################################
class StockPickersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = StockPickers
        fields = '__all__'
###############################################################################