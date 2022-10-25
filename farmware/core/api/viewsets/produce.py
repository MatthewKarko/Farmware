from http.client import responses
from django.db import IntegrityError
from django.http import QueryDict
import json
from django.forms.models import model_to_dict

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from ..models.produce import Produce, ProduceVariety, ProduceQuantitySuffix
from ..responses import DefaultResponses
from ..serialisers.produce import (
    ProduceSerialiser, 
    ProduceCreationSerialiser,
    ProduceFullSerialiser,
    ProduceVarietySerialiser,
    ProduceQuantitySuffixSerialiser
)
from ...permissions.IsOfficeOrHigherHierarchy import IsHigherThanWorkerHierarchy
from ...user.models import User
from ...user.permissions import IsInOrganisation


class ProduceViewSet(ModelViewSet):
    serializer_class = ProduceSerialiser
    responses = DefaultResponses(context='Produce')

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this viewset 
        requires."""

        # Not instantiated
        if self.action is None: return []

        # All others
        permission_classes = [IsAuthenticated, IsInOrganisation]

        # Updating or deleting information
        if self.action != 'retrieve' or self.action != 'list':
            permission_classes.append(IsHigherThanWorkerHierarchy)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Get the serialiser class for the appropriate action."""
        if self.action == 'create': return ProduceCreationSerialiser
        if self.action == 'retrieve': return ProduceFullSerialiser

        return super().get_serializer_class()

    def get_queryset(self, **kwargs):
        """Get all produce in the user's organisation."""
        user: User = self.request.user  # type: ignore
        return Produce.objects.all().filter(organisation=user.organisation, **kwargs)
    
    @action(detail=True, methods=['post'])
    def create_varieties(self, request, *args, **kwargs):
        data: QueryDict = request.data
        user: User = self.request.user
        varieties = json.loads(data['name'])
        if (len(varieties) == 0):
            return self.responses.BAD_REQUEST
        
        output = []
        prod = Produce.objects.all().filter(id=kwargs.get('pk'), organisation=user.organisation).first()
        if (prod != None):
            for name in varieties:
                obj = ProduceVariety(produce_id = prod, variety=name)
                obj.save()
                output.append(obj)

        if len(output) == 0:
            return self.responses.BAD_REQUEST

        return self.responses.list_json(output)

    def create(self, request, *args, **kwargs):
        """Create new produce."""
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
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.responses.DELETION_SUCCESS

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProduceVarietyViewSet(ModelViewSet):
    serializer_class = ProduceVarietySerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    responses = DefaultResponses(context='Produce Variety')

    def get_queryset(self, **kwargs):
        user: User = self.request.user  # type: ignore
        return ProduceVariety.objects.all().filter(produce_id__organisation=user.organisation, **kwargs)

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        print(data)
        serialiser = self.get_serializer(data=data, many=isinstance(request.data, list))
        serialiser.is_valid(raise_exception=True)
        try:
            serialiser.save()
        except IntegrityError as e:
            print('e (ProduceVarietyViewSet create):', e)
            return self.responses.RESPONSE_FORBIDDEN
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


class ProduceQuantitySuffixViewSet(ModelViewSet):
    serializer_class = ProduceQuantitySuffixSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    responses = DefaultResponses(context='Produce Quantity Suffix')

    def get_queryset(self, **kwargs):
        """Get all Produce Quantity Suffixes in the user's organisation."""
        user: User = self.request.user  # type: ignore
        return ProduceQuantitySuffix.objects.all().filter(
            produce_id__organisation=user.organisation, **kwargs)

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data

        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)
        try:
            serialiser.save()
        except IntegrityError as e:
            print('e (ProduceQuantitySuffixViewSet create):', e)
            return self.responses.RESPONSE_FORBIDDEN
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