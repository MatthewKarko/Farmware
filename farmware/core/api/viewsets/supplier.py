from django.http import QueryDict
from django.db import IntegrityError

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from core.api.responses import DefaultResponses

from ..models.supplier import Supplier
from ..serialisers.supplier import SupplierCreationSerialiser, SupplierSerialiser
from ...user.models import User
from ...user.permissions import IsInOrganisation

class SupplierViewSet(ModelViewSet):
    serializer_class = SupplierSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    responses = DefaultResponses('Supplier')

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return Supplier.objects.all().filter(organisation=user.organisation)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SupplierCreationSerialiser
        return SupplierSerialiser

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

    def list(self, request, *args, **kwargs):
        serialiser = SupplierSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.responses.DELETION_SUCCESS