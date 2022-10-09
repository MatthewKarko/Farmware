from urllib import request
from django.db import IntegrityError
from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..models import Produce
from ...user.models import User
from ..serialisers import ProduceSerialiser

class ProduceViewSet(ModelViewSet):
    serializer_class = ProduceSerialiser

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return Produce.objects.all().filter(
            organisation=user.organisation,
            **kwargs
        )

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        user: User = self.request.user
        data: QueryDict = request.data
        if user.organisation.code != data['organisation']:
            return Response({'error': 'You do not have access to the provided organisation.'}, status=status.HTTP_403_FORBIDDEN)

        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)

        try:
            serialiser.save()
        except IntegrityError:
            return Response({'error': 
            'A produce with the given name already exists in your organisation.'}, 
            status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Produce created.'}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        user: User = self.request.user
        data: QueryDict = request.data
        if user.organisation.code != data['organisation']:
            return Response({'error': 'You do not have access to the provided organisation.'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        user: User = self.request.user
        data: QueryDict = request.data
        if user.organisation.code != data['organisation']:
            return Response({'error': 'You do not have access to the provided organisation.'}, status=status.HTTP_403_FORBIDDEN)

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        super().destroy(request, *args, **kwargs)
        return Response({'success': 'Produce deleted.'}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to query for produce.'}, status=status.HTTP_403_FORBIDDEN)

        serialiser = ProduceSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)