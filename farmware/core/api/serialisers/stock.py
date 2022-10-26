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


class StockCreationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Stock
        exclude = ['organisation']

    def create(self, validated_data):
        validated_data['organisation'] = self.context['request'].user.organisation
        return Stock.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['organisation'] = self.context['request'].user.organisation
        return super().update(instance=instance, validated_data=validated_data)
###############################################################################


### STOCK PICKERS #############################################################
class StockFilteredSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['produce_id', 'variety_id']


class StockPickersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = StockPickers
        fields = '__all__'
###############################################################################
