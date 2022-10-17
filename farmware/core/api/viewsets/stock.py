from django.db import IntegrityError
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ...user.models import User
from ...user.permissions import IsInOrganisation
from ..models import Stock
from ..models import StockPickers
from ..serialisers import StockSerialiser
from ..serialisers import StockPickersSerialiser

class StockViewSet(ModelViewSet):
    serializer_class = StockSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    RESPONSE_FORBIDDEN = Response({'error': 'You are not an admin of the specified organisation.'}, status=status.HTTP_403_FORBIDDEN)
    RESPONSE_CREATION_SUCCESS = Response({'success': 'Stock created.'}, status=status.HTTP_200_OK)
    RESPONSE_DELETION_SUCCESS = Response({'success': 'Stock deleted.'}, status=status.HTTP_200_OK)

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return Stock.objects.all().filter(organisation=user.organisation, **kwargs)
    
    def valid_organisation(self, request):
        return request.user.organisation.code == request.data['organisation']

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        if not self.valid_organisation(request):
            return self.RESPONSE_FORBIDDEN
        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)
        try:
            serialiser.save()
        except IntegrityError:
            return self.RESPONSE_FORBIDDEN
        return self.RESPONSE_CREATION_SUCCESS
    
    def update(self, request, *args, **kwargs):
        if not self.valid_organisation(request):
            return self.RESPONSE_FORBIDDEN
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = StockSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.RESPONSE_DELETION_SUCCESS

class StockPickersViewSet(ModelViewSet):
    serializer_class = StockPickersSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    RESPONSE_DOES_NOT_EXIST = Response({'error': 'Stock Picker with the given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    RESPONSE_CREATION_SUCCESS = Response({'success': 'Stock Picker created.'}, status=status.HTTP_200_OK)
    RESPONSE_DELETION_SUCCESS = Response({'success': 'Stock Picker deleted.'}, status=status.HTTP_200_OK)

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return StockPickers.objects.all().filter(stock_id__organisation=user.organisation, **kwargs)

    def valid_organisation(self, request, data):
        return request.user.organisation == StockPickers.objects.get(id=data['stock_id']).organisation
    
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

    def partial_update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        try:
            if not self.valid_organisation(request, data):
                return self.RESPONSE_DOES_NOT_EXIST
        except ObjectDoesNotExist:
            return self.RESPONSE_DOES_NOT_EXIST
        super().partial_update(request, *args, **kwargs)
        return Response(self.get_serializer(data=data))

    def list(self, request, *args, **kwargs):
        serialiser = StockPickersSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.RESPONSE_DELETION_SUCCESS