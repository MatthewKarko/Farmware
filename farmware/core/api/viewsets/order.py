from django.db import IntegrityError
from django.http import QueryDict

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.api.models.customer import Customer

from ..models.order import (
    Order,
    OrderItem,
    OrderItemStockLink
)
from ..models import Produce, ProduceVariety, ProduceQuantitySuffix, Supplier, AreaCode
from ..models.stock import Stock
from ..responses import DefaultResponses
from ..serialisers.order import (
    OrderSerialiser,
    OrderCreationSerialiser,
    OrderFullSerialiser,
    OrderItemSerialiser,
    OrderItemDetailedSerialiser,
    OrderItemStockLinkSerialiser,
    OrderItemStockLinkAssignedStockSerialiser,
    OrderUpdateSerialiser
    )
from ..serialisers.stock import (
    StockSerialiser,
    BulkAddStockSerialiser
)
from ...user.models import User
from ...user.permissions import IsInOrganisation

def append_foreign_tables(user, obj):
    for item in obj:
        if 'produce_id' in item:
            produce = Produce.objects.all().filter(organisation=user.organisation).filter(id=item['produce_id']).first()
            if produce != None:
                item['produce_name'] = produce.name
            else:
                item['produce_name'] = "Unknown"

        if 'variety_id' in item:
            variety = ProduceVariety.objects.all().filter(id=item['variety_id']).first()
            if variety != None and variety.produce_id.pk == item['produce_id']:
                item['variety_name'] = variety.variety
            else:
                item['variety_name'] = "Unknown"

        if 'quantity_suffix_id' in item:
            quantity_suffix = ProduceQuantitySuffix.objects.all().filter(id=item['quantity_suffix_id']).first()
            if quantity_suffix != None and quantity_suffix.produce_id.pk == item['produce_id']:
                item['quantity_suffix_name'] = quantity_suffix.suffix
                item['base_equivalent'] = quantity_suffix.base_equivalent
            else:
                item['quantity_suffix_name'] = "Unknown"
                item['base_equivalent'] = 1
        
        if 'area_code_id' in item:
            area_code = AreaCode.objects.all().filter(id=item['area_code_id']).first()
            if area_code != None:
                item['area_code_name'] = area_code.area_code
                item['area_code_description'] = area_code.description
            else:
                item['area_code_name'] = "Unknown"
                item['area_code_description'] = "Unknown"

        if 'supplier_id' in item:
            supplier = Supplier.objects.all().filter(id=item['supplier_id']).first()
            if supplier != None:
                item['supplier_name'] = supplier.name
                item['supplier_phone_number'] = supplier.phone_number
            else:
                item['supplier_name'] = "Unknown"
                item['supplier_phone_number'] = "Unknown"
        
        if 'customer_id' in item:
            customer = Customer.objects.all().filter(id=item['customer_id']).first()
            if customer != None:
                item['customer_name'] = customer.name
                item['customer_phone_number'] = customer.phone_number
            else:
                item['customer_name'] = "Unknown"
                item['customer_phone_number'] = "Unknown"

### ORDER #####################################################################
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    responses = DefaultResponses('Order')

    def get_queryset(self, **kwargs):
        """Get all orders in the user's organisation."""
        user: User = self.request.user  # type: ignore
        return Order.objects.all().filter(
            organisation=user.organisation, **kwargs)

    def get_serializer_class(self):
        """Get the serialiser class for the appropriate action."""
        if self.action in ['create', 'update', 'partial_update']: return OrderCreationSerialiser
        if self.action == 'retrieve': return OrderFullSerialiser

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)
        item = None
        try:
            item = serialiser.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in e.args[0]:
                return self.responses.ITEM_ALREADY_EXISTS
            return self.responses.RESPONSE_FORBIDDEN
        return self.responses.json(item)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        obj = self.get_queryset().filter(id=kwargs.get('pk')).first()
        if obj == None:
            return self.responses.BAD_REQUEST
        serialiser = self.get_serializer(obj, data=data)
        serialiser.is_valid(raise_exception=True)
        item = serialiser.save()
        if item == None:
            return self.responses.BAD_REQUEST
        else:
            return self.responses.json(item)

    def partial_update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        obj = self.get_queryset().filter(id=kwargs.get('pk')).first()
        if obj == None:
            return self.responses.BAD_REQUEST
        serialiser = self.get_serializer(obj, data=data, partial=True)
        serialiser.is_valid(raise_exception=True)
        item = serialiser.save()
        if item == None:
            return self.responses.BAD_REQUEST
        else:
            return self.responses.json(item)

    def list(self, request, *args, **kwargs):
        user: User = request.user
        serialiser = OrderSerialiser(self.get_queryset(), many=True)
        append_foreign_tables(user, serialiser.data)
        return Response(serialiser.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.responses.DELETION_SUCCESS

    @action(detail=True, methods=['get'])
    def get_order_items(self, request, pk=None):
        order = self.get_object()
        user: User = request.user
        order_items = OrderItemDetailedSerialiser(
            OrderItem.objects.all().filter(order_id=order.id),
            many=True
            ).data
        append_foreign_tables(user, order_items)
        return Response({'order_items': order_items}, status=status.HTTP_200_OK)
###############################################################################


### ORDER ITEM ################################################################
class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerialiser
    permission_classes = [IsAuthenticated]
    responses = DefaultResponses('Order Item')

    def get_queryset(self, **kwargs):
        """Get all order items in the user's organisation."""
        user: User = self.request.user  # type: ignore
        return OrderItem.objects.all().filter(
            order_id__organisation=user.organisation, **kwargs
            )

    def get_serializer_class(self):
        """Get the serialiser class for the appropriate action."""
        if self.action == 'bulk_add_stock': return BulkAddStockSerialiser

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data

        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)

        try:
            serialiser.save()
        except IntegrityError as e:
            print('e (OrderItemViewSet create):', e)
            return self.responses.RESPONSE_FORBIDDEN

        return self.responses.CREATION_SUCCESS

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.responses.DELETION_SUCCESS

    def list(self, request, *args, **kwargs):
        user: User = request.user
        serialiser = OrderItemSerialiser(self.get_queryset(), many=True)
        append_foreign_tables(user, serialiser.data)
        return Response(serialiser.data)
    
    @action(detail=True, methods=['get'])
    def get_available_stock(self, request, pk=None):
        user: User = request.user
        order_item: OrderItem = self.get_object()

        data = StockSerialiser(Stock.objects.all().filter(
            produce_id=order_item.produce_id, 
            variety_id=order_item.produce_variety_id,
            date_completed__isnull=True
            ), many=True
        ).data
        append_foreign_tables(user, data)
        response = {'stock':data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_assigned_stock(self, request, pk=None):
        order_item: OrderItem = self.get_object()

        data = OrderItemStockLinkAssignedStockSerialiser(OrderItemStockLink.objects.all().filter(
            order_item_id=order_item.pk
            ), many=True
        ).data
        # append_foreign_tables(user, data)
        response = {'stock':data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def bulk_add_stock(self, request, pk=None):
        order_item: OrderItem = self.get_object()
        data: QueryDict = request.data

        serialiser: BulkAddStockSerialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)
        for stock_item in serialiser.validated_data.get('items'):  # type: ignore
            # Create new order item stock link (OrderItemStockLink)
            OrderItemStockLink.objects.create(
                order_item_id=order_item.pk,
                stock_id = stock_item.stock_id,
                quantity = stock_item.quantity,
                quantity_suffix_id = stock_item.quantity_suffix_id
            )

        return Response(serialiser.data, status=status.HTTP_200_OK)
###############################################################################


### ORDER ITEM STOCK LINK #####################################################
class OrderItemStockLinkViewSet(ModelViewSet):
    serializer_class = OrderItemStockLinkSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    responses = DefaultResponses('Order Item Stock Link')

    def get_queryset(self, **kwargs):
        """Get all order item stock links in the user's organisation."""
        user: User = self.request.user  # type: ignore
        return OrderItemStockLink.objects.all().filter(
            order_item_id__order_id__organisation=user.organisation, **kwargs
            )

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data

        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)

        try:
            serialiser.save()
        except IntegrityError as e:
            print('e (OrderItemStockLinkViewSet create):', e)
            return self.responses.RESPONSE_FORBIDDEN

        return self.responses.CREATION_SUCCESS

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.responses.DELETION_SUCCESS

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
###############################################################################