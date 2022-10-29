from django.http import QueryDict
from django.db import IntegrityError

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

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
        if self.action in ['create', 'update', 'partial_update']:
            return CustomerCreationSerialiser
        # TODO:
        # if self.action == 'retrieve': return OrderFullSerialiser

        # if 'update' in self.action: return OrderUpdateSerialiser

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)
        item = None
        try:
            item = serialiser.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in e.args[0]:
                return self.responses.ITEM_ALREADY_EXISTS
            return self.responses.RESPONSE_FORBIDDEN
        return self.responses.json(item)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        obj = self.get_queryset().filter(id=kwargs.get('pk')).first()
        if obj == None:
            return self.responses.BAD_REQUEST
        serialiser = self.get_serializer(obj, data=data)
        serialiser.is_valid(raise_exception=True)
        item = serialiser.save()
        if item == None:
            return self.responses.BAD_REQUEST
        else:
            return self.responses.json(item)

    def partial_update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        obj = self.get_queryset().filter(id=kwargs.get('pk')).first()
        if obj == None:
            return self.responses.BAD_REQUEST
        serialiser = self.get_serializer(obj, data=data, partial=True)
        serialiser.is_valid(raise_exception=True)
        item = serialiser.save()
        if item == None:
            return self.responses.BAD_REQUEST
        else:
            return self.responses.json(item)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.responses.DELETION_SUCCESS

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)