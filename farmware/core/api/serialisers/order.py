from rest_framework import serializers

from ..models.customer import Customer
from ..models.order import Order, OrderItem, OrderItemStockLink

### ORDER #####################################################################
class OrderSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderCreationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer_id', 'invoice_number']


class OrderFullSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer_id', 'invoice_number']

    def to_representation(self, data):
        data = super(OrderFullSerialiser, self).to_representation(data)

        data['customer_name'] = Customer.objects.get(
            id=data['customer_id']).name

        data['order_items'] = []
        # ProduceVarietyInOrganisationSerialiser(
        #     ProduceVariety.objects.all().filter(produce_id=data.get('id')), 
        #     many=True
        #     ).data
        return data
###############################################################################


### ORDER ITEM ################################################################
class OrderItemSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
###############################################################################


### ORDER ITEM STOCK LINK #####################################################
class OrderItemStockLinkSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderItemStockLink
        fields = '__all__'
###############################################################################