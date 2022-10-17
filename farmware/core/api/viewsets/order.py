from django.db import IntegrityError
from django.http import QueryDict

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models.order import (
    Order,
    OrderItem,
    OrderItemStockLink
)
from ..responses import DefaultResponses
from ..serialisers.order import (
    OrderSerialiser,
    OrderCreationSerialiser,
    OrderFullSerialiser,
    OrderItemSerialiser,
    OrderItemStockLinkSerialiser,
    OrderUpdateSerialiser
    )
from ...user.models import User
from ...user.permissions import IsInOrganisation


### ORDER #####################################################################
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    responses = DefaultResponses('Order')

    def get_queryset(self, **kwargs):
        """Get all orders in the user's organisation."""
        print(self.serializer_class.Meta.model)
        user: User = self.request.user  # type: ignore
        return Order.objects.all().filter(
            organisation=user.organisation, **kwargs)

    def get_serializer_class(self):
        """Get the serialiser class for the appropriate action."""
        if self.action == 'create': return OrderCreationSerialiser
        if self.action == 'retrieve': return OrderFullSerialiser

        if 'update' in self.action: return OrderUpdateSerialiser

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data

        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)

        try:
            serialiser.save()
        except IntegrityError as e:
            print('OrderViewSet (create):', e)
            return self.responses.RESPONSE_FORBIDDEN
        return self.responses.CREATION_SUCCESS

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = OrderSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.responses.DELETION_SUCCESS

    @action(detail=True, methods=['get'])
    def get_order_items(self, request, pk=None):
        order = self.get_object()

        data: QueryDict = request.data

        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)

        order_items = OrderItemSerialiser(
            OrderItem.objects.all().filter(order_id=order.id),
            many=True
            ).data

        return Response({'order_items': order_items}, status=status.HTTP_200_OK)
###############################################################################


### ORDER ITEM ################################################################
class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    responses = DefaultResponses('Order Item')

    def get_queryset(self, **kwargs):
        """Get all order items in the user's organisation."""
        user: User = self.request.user  # type: ignore
        return OrderItem.objects.all().filter(
            order_id__organisation=user.organisation, **kwargs
            )

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
        return super().list(request, *args, **kwargs)
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
            order_id__organisation=user.organisation, **kwargs
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