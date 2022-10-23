from django.db import IntegrityError
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action

from core.api.responses import DefaultResponses

from ..models.stock import Stock, StockPickers
from ..serialisers.stock import StockSerialiser, StockPickersSerialiser, StockFilteredSerialiser
from ...user.models import User
from ...user.permissions import IsInOrganisation

class StockViewSet(ModelViewSet):
    serializer_class = StockSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    responses = DefaultResponses('Stock')

    def get_serializer_class(self):
        if self.action == 'list_filtered':
            return StockFilteredSerialiser
        return StockSerialiser

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        objects = Stock.objects.all().filter(organisation=user.organisation, **kwargs)
        if self.action == 'list_filtered':
            data: QueryDict = self.request.data
            return objects.filter(produce_id=data['produce_id'], **kwargs).filter(variety_id=data['variety_id'], **kwargs)
        return objects
    
    def valid_organisation(self, request):
        return request.user.organisation.code == request.data['organisation']

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        if not self.valid_organisation(request):
            return self.responses.RESPONSE_FORBIDDEN
        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)
        try:
            serialiser.save()
        except IntegrityError:
            return self.responses.RESPONSE_FORBIDDEN
        return self.responses.CREATION_SUCCESS
    
    def update(self, request, *args, **kwargs):
        if not self.valid_organisation(request):
            return self.responses.RESPONSE_FORBIDDEN
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = StockSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)

    @action(detail=False, methods=['post'])
    def list_filtered(self, request, *args, **kwargs):
        serialiser = StockSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.responses.DELETION_SUCCESS

class StockPickersViewSet(ModelViewSet):
    serializer_class = StockPickersSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    responses = DefaultResponses('Stock Pickers')

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return StockPickers.objects.all().filter(stock_id__organisation=user.organisation, **kwargs)

    def valid_organisation(self, request, data):
        return request.user.organisation == StockPickers.objects.get(id=data['stock_id']).organisation
    
    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        try:
            if not self.valid_organisation(request, data):
                return self.responses.DOES_NOT_EXIST
        except ObjectDoesNotExist:
            return self.responses.DOES_NOT_EXIST
        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)
        try:
            serialiser.save()
        except IntegrityError:
            return self.responses.DOES_NOT_EXIST
        return self.responses.CREATION_SUCCESS

    def update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        try:
            if not self.valid_organisation(request, data):
                return self.responses.DOES_NOT_EXIST
        except ObjectDoesNotExist:
            return self.responses.DOES_NOT_EXIST
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        try:
            if not self.valid_organisation(request, data):
                return self.responses.DOES_NOT_EXIST
        except ObjectDoesNotExist:
            return self.responses.DOES_NOT_EXIST
        super().partial_update(request, *args, **kwargs)
        return Response(self.get_serializer(data=data))

    def list(self, request, *args, **kwargs):
        serialiser = StockPickersSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.responses.DELETION_SUCCESS