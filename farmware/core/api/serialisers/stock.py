from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .fields.stock import StockListField
from ..models.stock import Stock, StockPickers


### STOCK #####################################################################
class StockSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class StockFilteredSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['produce_id', 'variety_id']


class BulkAddStockSerialiser(serializers.ModelSerializer):
    items = StockListField()
    class Meta:
        model = Stock
        fields = ['items']

    def validate_items(self, items):
        for item in items:
            stock = item.get('stock')
            if stock.date_completed is not None:
                raise serializers.ValidationError(f'Stock ({stock.pk}) has been completed.')
        return items



class StockCreationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Stock
        exclude = ['organisation']

    def create(self, validated_data):
        validated_data['organisation'] = self.context['request'].user.organisation
        validated_data['quantity_available'] = validated_data['quantity']
        return Stock.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['organisation'] = self.context['request'].user.organisation
        return super().update(instance=instance, validated_data=validated_data)
###############################################################################


### STOCK PICKERS #############################################################
class StockPickersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = StockPickers
        fields = '__all__'
###############################################################################
