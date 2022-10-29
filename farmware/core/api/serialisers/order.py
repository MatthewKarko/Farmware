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
        exclude = ['organisation']

    def create(self, validated_data):        
        # Add organisational data
        validated_data['organisation'] = self.context['request'].user.organisation
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['organisation'] = self.context['request'].user.organisation
        return super().update(instance=instance, validated_data=validated_data)


class OrderUpdateSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer_id', 'invoice_number']


class OrderFullSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'invoice_number']

    def to_representation(self, data):
        data = super(OrderFullSerialiser, self).to_representation(data)

        data['customer_name'] = Customer.objects.get(
            id=data['customer_id']).name

        # TODO: fix?
        data['order_items'] = OrderItemListSerialiser(
            OrderItem.objects.all().filter(order_id=data.get('id')), 
            many=True
            ).data
        return data
###############################################################################


### ORDER ITEM ################################################################
class OrderItemSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'#['quantity', 'quantity_suffix_id']
###############################################################################


### ORDER ITEM STOCK LINK #####################################################
class OrderItemStockLinkSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderItemStockLink
        fields = '__all__'
###############################################################################