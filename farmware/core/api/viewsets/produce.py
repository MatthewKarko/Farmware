from django.db import IntegrityError
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ...user.models import User
from ...user.permissions import IsInOrganisation
from ..models import Produce
from ..models import ProduceVariety
from ..models import ProduceQuantitySuffix
from ..serialisers import ProduceSerialiser
from ..serialisers import ProduceVarietySerialiser
from ..serialisers import ProduceQuantitySuffixSerialiser

class ProduceViewSet(ModelViewSet):
    serializer_class = ProduceSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    RESPONSE_FORBIDDEN = Response({'error': 'You are not an admin of the specified organisation.'}, status=status.HTTP_403_FORBIDDEN)
    RESPONSE_CREATION_SUCCESS = Response({'success': 'Produce created.'}, status=status.HTTP_200_OK)
    RESPONSE_DELETION_SUCCESS = Response({'success': 'Produce deleted.'}, status=status.HTTP_200_OK)

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return Produce.objects.all().filter(organisation=user.organisation, **kwargs)

    def valid_organisation(self, request, data):
        return request.user.organisation.code == data['organisation']

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        if not self.valid_organisation(request, data):
            return self.RESPONSE_FORBIDDEN
        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)
        try:
            serialiser.save()
        except IntegrityError:
            return self.RESPONSE_FORBIDDEN
        return self.RESPONSE_CREATION_SUCCESS

    def update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        if not self.valid_organisation(request, data):
            return self.RESPONSE_FORBIDDEN
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = ProduceSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.RESPONSE_DELETION_SUCCESS

class ProduceVarietyViewSet(ModelViewSet):
    serializer_class = ProduceVarietySerialiser
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    RESPONSE_DOES_NOT_EXIST = Response({'error': 'Produce with the given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    RESPONSE_CREATION_SUCCESS = Response({'success': 'Produce Variety created.'}, status=status.HTTP_200_OK)
    RESPONSE_DELETION_SUCCESS = Response({'success': 'Produce Variety deleted.'}, status=status.HTTP_200_OK)

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return ProduceVariety.objects.all().filter(produce_id__organisation=user.organisation, **kwargs)

    def valid_organisation(self, request, data):
        return request.user.organisation == Produce.objects.get(id=data['produce_id']).organisation

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
        serialiser = ProduceVarietySerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.RESPONSE_DELETION_SUCCESS

class ProduceQuantitySuffixViewSet(ModelViewSet):
    serializer_class = ProduceQuantitySuffixSerialiser
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    RESPONSE_DOES_NOT_EXIST = Response({'error': 'Produce with the given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    RESPONSE_CREATION_SUCCESS = Response({'success': 'Produce Quantity Suffix created.'}, status=status.HTTP_200_OK)
    RESPONSE_DELETION_SUCCESS = Response({'success': 'Produce Quantity Suffix deleted.'}, status=status.HTTP_200_OK)

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return ProduceQuantitySuffix.objects.all().filter(produce_id__organisation=user.organisation, **kwargs)

    def valid_organisation(self, request, data):
        return request.user.organisation == Produce.objects.get(id=data['produce_id']).organisation

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
        serialiser = ProduceQuantitySuffixSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.RESPONSE_DELETION_SUCCESS