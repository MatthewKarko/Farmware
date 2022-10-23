from django.db import IntegrityError
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action

from core.api.responses import DefaultResponses

from ..models import Produce, ProduceVariety, ProduceQuantitySuffix, AreaCode, Supplier
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

    def append_foreign_tables(self, user, obj):
        for item in obj:
            produce = Produce.objects.all().filter(organisation=user.organisation).filter(id=item['produce_id']).first()
            if produce != None:
                item['produce_name'] = produce.name
            else:
                item['produce_name'] = "Unknown"

            variety = ProduceVariety.objects.all().filter(id=item['variety_id']).first()
            if variety != None and variety.produce_id.id == item['produce_id']:
                item['variety_name'] = variety.variety
            else:
                item['variety_name'] = "Unknown"

            quantity_suffix = ProduceQuantitySuffix.objects.all().filter(id=item['quantity_suffix_id']).first()
            if quantity_suffix != None and quantity_suffix.produce_id.id == item['produce_id']:
                item['quantity_suffix_name'] = quantity_suffix.suffix
                item['base_equivalent'] = quantity_suffix.base_equivalent
            else:
                item['quantity_suffix_name'] = "Unknown"
                item['base_equivalent'] = 1
            
            area_code = AreaCode.objects.all().filter(id=item['area_code_id']).first()
            if area_code != None:
                item['area_code_name'] = area_code.area_code
                item['area_code_description'] = area_code.description
            else:
                item['area_code_name'] = "Unknown"
                item['area_code_description'] = "Unknown"

            supplier = Supplier.objects.all().filter(id=item['supplier_id']).first()
            if supplier != None:
                item['supplier_name'] = supplier.name
                item['supplier_phone_number'] = supplier.phone_number
            else:
                item['supplier_name'] = "Unknown"
                item['supplier_phone_number'] = "Unknown"

    def list(self, request, *args, **kwargs):
        serialiser = StockSerialiser(self.get_queryset(), many=True)
        self.append_foreign_tables(user, serialiser.data)
        return Response(serialiser.data)

    @action(detail=False, methods=['post'])
    def list_filtered(self, request, *args, **kwargs):
        user: User = self.request.user
        serialiser = StockSerialiser(self.get_queryset(), many=True)
        self.append_foreign_tables(user, serialiser.data)
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