from rest_framework import serializers

from ..models.customer import Customer
from ..models.order import Order
from ..models.order import OrderStock

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

        data['customer_name'] = Customer.objects.get(id=data['customer_id']).name

        data['order_items'] = []
        # ProduceVarietyInOrganisationSerialiser(
        #     ProduceVariety.objects.all().filter(produce_id=data.get('id')), 
        #     many=True
        #     ).data
        return data
###############################################################################


### ORDER STOCK ###############################################################
class OrderStockSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderStock
        fields = '__all__'
###############################################################################