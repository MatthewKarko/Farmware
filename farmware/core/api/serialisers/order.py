from django.db.models import F, Sum

from rest_framework import serializers

from ..models.customer import Customer
from ..models.produce import Produce, ProduceQuantitySuffix, ProduceVariety
from ..models.order import Order, OrderItem, OrderItemStockLink
from ..models.stock import Stock

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


class OrderItemDetailedSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def to_representation(self, instance):
        data = super(OrderItemDetailedSerialiser, self).to_representation(instance)

        # Get sum all quantity in base equivalent form
        quantity_used = OrderItemStockLink.objects.filter(
            order_item_id=data['id']
        ).aggregate(quantity_used=Sum( 
            F('quantity') *  F('quantity_suffix_id__base_equivalent')
            ))['quantity_used']

        # TODO: see if there is an easier way to reference the current instance 
        #       rather than querying.
        order_item: OrderItem = OrderItem.objects.get(id=data['id'])

        # Convert to relative form
        if quantity_used is not None:
            quantity_suffix: ProduceQuantitySuffix = order_item.quantity_suffix_id
            base_equivalent = quantity_suffix.base_equivalent
            quantity_used = quantity_used / base_equivalent
        else:
            quantity_used = 0

        data['quantity_used'] = quantity_used

        # Add variety_name
        variety: ProduceVariety = order_item.produce_variety_id
        data['variety_name'] = variety.variety

        return data


class OrderItemListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
###############################################################################


### ORDER ITEM STOCK LINK #####################################################
class OrderItemStockLinkSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderItemStockLink
        fields = '__all__'


class OrderItemStockLinkAssignedStockSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderItemStockLink
        fields = ['id', 'quantity', 'stock_id', 'quantity_suffix_id']

    def to_representation(self, data):
        data = super(OrderItemStockLinkAssignedStockSerialiser, self).to_representation(data)

        stock: Stock = Stock.objects.get(id=data['stock_id'])
        produce: Produce = stock.produce_id
        variety: ProduceVariety = stock.variety_id
        
        data['produce_name'] = produce.name
        data['produce_variety'] = variety.variety
        data['quantity_suffix'] = ProduceQuantitySuffix.objects.get(id=data['quantity_suffix_id']).suffix

        return data
###############################################################################