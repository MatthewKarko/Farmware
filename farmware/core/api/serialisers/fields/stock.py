from rest_framework import serializers


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