from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from ..models.stock import Stock, StockPickers

# TODO: move
class AddStockField(serializers.Field):

    default_error_messages = {
    'not_provided': "'{context}' is not provided.",
    'wrong_type': "'{context}' is not of type {type}."
}

    def to_representation(self, value):
        return {
            'stock_id': value.get('stock_id'),
            'quantity': value.get('quantity')
        }

    def to_internal_value(self, data: dict):
        if data.get('stock_id', False) is False: 
            self.fail('not_provided', context='stock_id')
        if data.get('quantity', False) is False: 
            self.fail('not_provided', context='quantity')

        try:
            float(data.get('quantity'))  # type: ignore
        except ValueError:
            self.fail('wrong_type', context='quantity', type='float')

        return {
            'stock_id': data['stock_id'],
            'quantity': float(data['quantity'])
        }

class StockListField(serializers.ListField):
    child = AddStockField()


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
            stock_id = item.get('stock_id')
            try:
                stock = Stock.objects.get(
                    organisation=self.context['request'].user.organisation,
                    id=stock_id
                )

                if stock.date_completed is not None:
                    raise serializers.ValidationError(f'Stock ({stock_id}) has been completed.')

            except ObjectDoesNotExist:
                raise serializers.ValidationError(f'Stock ({stock_id}) does not exist.')
        return items



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
class StockPickersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = StockPickers
        fields = '__all__'
###############################################################################
