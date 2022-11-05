from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from ...models.produce import ProduceQuantitySuffix
from ...models.stock import Stock


class AddStockField(serializers.Field):

    default_error_messages = {
    'not_provided': "'{context}' is not provided.",
    'wrong_type': "'{context}' is not of type {type}.",
    'does_not_exist': "The {context} ({id}) provided does not exist.",
}

    def to_representation(self, value):
        return {
            'stock_id': value.get('stock').pk,
            'quantity': value.get('quantity'),
            'quantity_suffix_id': value.get('quantity_suffix').pk
        }

    def to_internal_value(self, data: dict):
        if data.get('stock_id', False) is False: 
            self.fail('not_provided', context='stock_id')
        if data.get('quantity', False) is False: 
            self.fail('not_provided', context='quantity')

        # Quantity
        try:
            float(data.get('quantity'))  # type: ignore
        except ValueError:
            self.fail('wrong_type', context='quantity', type='float')

        # Get the objects
        try:
            stock = Stock.objects.get(id=data['stock_id'])
        except ObjectDoesNotExist:
            self.fail('does_not_exist', context='stock_id', id=data['stock_id'])

        try:
            quantity_suffix = ProduceQuantitySuffix.objects.get(
                id=data['quantity_suffix_id'])
        except ObjectDoesNotExist:
            self.fail('does_not_exist', context='quantity_suffix_id', id=data['quantity_suffix_id'])

        return {
            'stock': stock,
            'quantity': float(data['quantity']),
            'quantity_suffix': quantity_suffix
        }

class StockListField(serializers.ListField):
    child = AddStockField()