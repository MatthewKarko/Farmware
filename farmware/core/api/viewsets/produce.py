from django.db import IntegrityError
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ...user.models import User
from ...user.permissions import IsInOrganisation
from ..models.produce import Produce, ProduceVariety, ProduceQuantitySuffix
from ..serialisers.produce import (
    ProduceSerialiser, 
    ProduceCreationSerialiser,
    ProduceFullSerialiser,
    ProduceVarietySerialiser,
    ProduceQuantitySuffixSerialiser
)

class ProduceViewSet(ModelViewSet):
    serializer_class = ProduceSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    RESPONSE_FORBIDDEN = Response({'error': 'You are not an admin of the specified organisation.'}, status=status.HTTP_403_FORBIDDEN)
    RESPONSE_CREATION_SUCCESS = Response({'success': 'Produce created.'}, status=status.HTTP_201_CREATED)
    RESPONSE_DELETION_SUCCESS = Response({'success': 'Produce deleted.'}, status=status.HTTP_200_OK)

    def get_queryset(self, **kwargs):
        """Get all produce in the user's organisation."""
        user: User = self.request.user  # type: ignore
        return Produce.objects.all().filter(organisation=user.organisation, **kwargs)

    def get_serializer_class(self):
        """Get the serialiser class for the appropriate action."""
        if self.action == 'create': return ProduceCreationSerialiser
        if self.action == 'retrieve': return ProduceFullSerialiser

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """Create new produce."""
        data: QueryDict = request.data

        serialiser = self.get_serializer(data=data)  # type: ignore
        serialiser.is_valid(raise_exception=True)
        try:
            serialiser.save()
        except IntegrityError as e:
            return Response({'error': e}, status=status.HTTP_403_FORBIDDEN)
        return self.RESPONSE_CREATION_SUCCESS

    def update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = ProduceSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.RESPONSE_DELETION_SUCCESS

    def retrieve(self, request, *args, **kwargs):
        # TODO: add extra information
        return super().retrieve(request, *args, **kwargs)

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