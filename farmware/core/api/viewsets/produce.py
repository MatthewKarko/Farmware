from django.db import IntegrityError
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ...user.models import User
from ...user.permissions import IsInOrganisation
from ...user.permissions import IsInProduceForeignKeyOrganisation

from ..models import Produce
from ..models import ProduceVariety
from ..models import ProduceQuantitySuffix

from ..serialisers import ProduceSerialiser
from ..serialisers import ProduceVarietySerialiser
from ..serialisers import ProduceQuantitySuffixSerialiser

class ProduceViewSet(ModelViewSet):
    serializer_class = ProduceSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return Produce.objects.all().filter(
            organisation=user.organisation,
            **kwargs
        )

    def create(self, request, *args, **kwargs):
        user: User = self.request.user
        data: QueryDict = request.data
        if (user.organisation != data['organisation']):
            return Response({'error': 'You are not an admin of the specific organisation.'}, status=status.HTTP_403_FORBIDDEN)

        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)

        try:
            serialiser.save()
        except IntegrityError:
            return Response({'error': 
            'A produce with the given name already exists in your organisation.'}, 
            status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Produce created.'}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user: User = self.request.user
        data: QueryDict = request.data
        if user.organisation.code != data['organisation']:
            return Response({'error': 'You do not have access to the provided organisation.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = ProduceSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': 'Produce deleted.'}, status=status.HTTP_200_OK)

class ProduceVarietyViewSet(ModelViewSet):
    serializer_class = ProduceVarietySerialiser
    permission_classes = [IsAuthenticated, IsInProduceForeignKeyOrganisation]

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return ProduceVariety.objects.all().filter(
            produce_id__organisation=user.organisation,
            **kwargs
        )

    def create(self, request, *args, **kwargs):
        user: User = self.request.user
        data: QueryDict = request.data

        try:
            if user.organisation != Produce.objects.get(id=data['produce_id']).organisation:
                return Response({'error': 'Produce with given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response({'error': 'Produce with given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)

        try:
            serialiser.save()
        except IntegrityError:
            return Response({'error': 
            'A produce variety with the given name already exists in your organisation.'}, 
            status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Produce variety created.'}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user: User = self.request.user
        data: QueryDict = request.data

        try:
            if user.organisation != Produce.objects.get(id=data['produce_id']).organisation:
                return Response({'error': 'Produce with given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response({'error': 'Produce with given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = ProduceVarietySerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': 'Produce variety deleted.'}, status=status.HTTP_200_OK)

class ProduceQuantitySuffixViewSet(ModelViewSet):
    serializer_class = ProduceQuantitySuffixSerialiser
    permission_classes = [IsAuthenticated, IsInProduceForeignKeyOrganisation]

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return ProduceQuantitySuffix.objects.all().filter(
            produce_id__organisation=user.organisation,
            **kwargs
        )

    def create(self, request, *args, **kwargs):
        user: User = self.request.user
        data: QueryDict = request.data

        try:
            if user.organisation != Produce.objects.get(id=data['produce_id']).organisation:
                return Response({'error': 'Produce with given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response({'error': 'Produce with given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)

        try:
            serialiser.save()
        except IntegrityError:
            return Response({'error': 
            'A produce quantity suffix with the given name already exists in your organisation.'}, 
            status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Produce quantity suffix created.'}, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        user: User = self.request.user
        data: QueryDict = request.data

        try:
            if user.organisation != Produce.objects.get(id=data['produce_id']).organisation:
                return Response({'error': 'Produce with given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response({'error': 'Produce with given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = ProduceQuantitySuffixSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': 'Produce quantity suffix deleted.'}, status=status.HTTP_200_OK)