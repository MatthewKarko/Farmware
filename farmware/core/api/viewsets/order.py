from django.db import IntegrityError
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..responses import DefaultResponses

from ...user.models import User
from ...user.permissions import IsInOrganisation
from ..models import Order
from ..models import OrderStock
from ..serialisers import OrderSerialiser
from ..serialisers import OrderStockSerialiser

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    responses = DefaultResponses('Order')

    def get_queryset(self, **kwargs):
        """Get all orders in the user's organisation."""
        user: User = self.request.user  # type: ignore
        return Order.objects.all().filter(organisation=user.organisation, **kwargs)

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)
        try:
            serialiser.save()
        except IntegrityError:
            return self.RESPONSE_FORBIDDEN
        return self.RESPONSE_CREATION_SUCCESS

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not self.valid_organisation(request):
            return self.RESPONSE_FORBIDDEN
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = OrderSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.RESPONSE_DELETION_SUCCESS

class OrderStockViewSet(ModelViewSet):
    serializer_class = OrderStockSerialiser
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    RESPONSE_DOES_NOT_EXIST = Response({'error': 'Order with the given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    RESPONSE_CREATION_SUCCESS = Response({'success': 'Order Stock created.'}, status=status.HTTP_200_OK)
    RESPONSE_DELETION_SUCCESS = Response({'success': 'Order Stock deleted.'}, status=status.HTTP_200_OK)

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return OrderStock.objects.all().filter(order_id__organisation=user.organisation, **kwargs)

    def valid_organisation(self, request, data):
        return request.user.organisation == Order.objects.get(id=data['order_id']).organisation

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        try:
            if not self.valid_organisation(request, data):
                return self.RESPONSE_DOES_NOT_EXIST
        except ObjectDoesNotExist:
            return self.RESPONSE_DOES_NOT_EXIST
        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)
        try:
            serialiser.save()
        except IntegrityError:
            return self.RESPONSE_DOES_NOT_EXIST
        return self.RESPONSE_CREATION_SUCCESS

    def update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        try:
            if not self.valid_organisation(request, data):
                return self.RESPONSE_DOES_NOT_EXIST
        except ObjectDoesNotExist:
            return self.RESPONSE_DOES_NOT_EXIST

        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = OrderStockSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.RESPONSE_DELETION_SUCCESS