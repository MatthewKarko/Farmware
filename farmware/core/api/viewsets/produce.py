from django.db import IntegrityError
from django.http import QueryDict
import json

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from ..models.produce import Produce, ProduceVariety, ProduceQuantitySuffix
from ..responses import DefaultResponses
from ..serialisers.produce import (
    ProduceQuantitySuffixUpdateSerialiser,
    ProduceSerialiser,
    ProduceCreationSerialiser,
    ProduceFullSerialiser,
    ProduceVarietySerialiser,
    ProduceQuantitySuffixSerialiser,
    ProduceVarietyUpdateSerialiser
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
        if self.action in ['create', 'update', 'partial_update']: return ProduceCreationSerialiser
        if self.action == 'retrieve': return ProduceFullSerialiser

        return super().get_serializer_class()

    def get_queryset(self, **kwargs):
        """Get all produce in the user's organisation."""
        user: User = self.request.user  # type: ignore
        return Produce.objects.all().filter(organisation=user.organisation, **kwargs)

    @action(detail=True, methods=['get'])
    def get_varieties(self, request, *args, **kwargs):
        user: User = self.request.user  # type: ignore
        prod = (Produce.objects.all().filter(id=kwargs.get('pk'), organisation=user.organisation)).first()
        if (prod == None):
            return self.responses.DOES_NOT_EXIST

        varieties = ProduceVariety.objects.all().filter(produce_id=kwargs.get('pk'))
        return self.responses.list_json(varieties)

    @action(detail=True, methods=['get'])
    def get_suffixes(self, request, *args, **kwargs):
        user: User = self.request.user  # type: ignore
        prod = (Produce.objects.all().filter(id=kwargs.get('pk'), organisation=user.organisation)).first()
        if (prod == None):
            return self.responses.DOES_NOT_EXIST

        suffixes = ProduceQuantitySuffix.objects.all().filter(produce_id=kwargs.get('pk'))
        return self.responses.list_json(suffixes)

    @action(detail=True, methods=['post'])
    def create_varieties(self, request, *args, **kwargs):
        data: QueryDict = request.data
        user: User = self.request.user  # type: ignore
        varieties = json.loads(data['name'].replace("\'", "\""))
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


class ProduceVarietyViewSet(ModelViewSet):
    serializer_class = ProduceVarietySerialiser
    permission_classes = [IsAuthenticated]
    responses = DefaultResponses(context='Produce Variety')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return ProduceVariety.objects.all().filter(produce_id__organisation=user.organisation)

    def get_serializer_class(self):
        if self.action == "partial_update":
            return ProduceVarietyUpdateSerialiser
        else:
            return ProduceVarietySerialiser

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        is_list = isinstance(data, list)
        serialiser = self.get_serializer(data=data, many=is_list)
        serialiser.is_valid(raise_exception=True)
        item = None
        try:
            item = serialiser.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in e.args[0]:
                return self.responses.ITEM_ALREADY_EXISTS
            return self.responses.RESPONSE_FORBIDDEN
        if is_list:
            return self.responses.list_json(item)
        return self.responses.json(item)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

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


class ProduceQuantitySuffixViewSet(ModelViewSet):
    serializer_class = ProduceQuantitySuffixSerialiser
    permission_classes = [IsAuthenticated]
    responses = DefaultResponses(context='Produce Quantity Suffix')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self, **kwargs):
        """Get all Produce Quantity Suffixes in the user's organisation."""
        user: User = self.request.user
        return ProduceQuantitySuffix.objects.all().filter(produce_id__organisation=user.organisation)

    def get_serializer_class(self):
        if self.action == "partial_update":
            return ProduceQuantitySuffixUpdateSerialiser
        else:
            return ProduceQuantitySuffixSerialiser

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        is_list = isinstance(data, list)
        serialiser = self.get_serializer(data=data, many=is_list)
        serialiser.is_valid(raise_exception=True)
        item = None
        try:
            item = serialiser.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in e.args[0]:
                return self.responses.ITEM_ALREADY_EXISTS
            return self.responses.RESPONSE_FORBIDDEN
        if is_list:
            return self.responses.list_json(item)
        return self.responses.json(item)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

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
