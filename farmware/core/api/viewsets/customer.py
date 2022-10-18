from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..responses import DefaultResponses
from ..models.customer import Customer
from ..serialisers.customer import (
    CustomerSerialiser,
    CustomerCreationSerialiser
)
from ...user.models import User
from ...user.permissions import IsInOrganisation

class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    responses = DefaultResponses('Customer')
    
    def get_queryset(self, **kwargs):
        """Get all customers in the user's organisation."""
        user: User = self.request.user  # type: ignore
        return Customer.objects.all().filter(
            organisation=user.organisation, **kwargs)

    def get_serializer_class(self):
        """Get the serialiser class for the appropriate action."""
        if self.action == 'create': return CustomerCreationSerialiser
        # if self.action == 'retrieve': return OrderFullSerialiser

        # if 'update' in self.action: return OrderUpdateSerialiser

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        print('create')
        data: QueryDict = request.data
        print('data:', data)

        serialiser = self.get_serializer(data=data)
        print('serialiser:', serialiser)
        serialiser.is_valid(raise_exception=True)

        serialiser.save()
        print('serialiser save:', serialiser)

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