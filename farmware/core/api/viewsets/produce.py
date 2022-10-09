from django.db import IntegrityError
from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..models import Produce
from ...user.models import User
from ...user.permissions import IsInOrganisation
from ..serialisers import ProduceSerialiser

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
        data: QueryDict = request.data

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
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        user: User = self.request.user
        data: QueryDict = request.data
        return super().partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = ProduceSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)