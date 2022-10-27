from django.db import IntegrityError
from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from core.api.responses import DefaultResponses

from ...user.models import User
from ...user.permissions import IsInOrganisation
from ..models import AreaCode
from ..serialisers.areacode import AreaCodeCreationSerialiser, AreaCodeSerialiser

class AreaCodeViewSet(ModelViewSet):
    serializer_class = AreaCodeSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    responses = DefaultResponses('Area Code')

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return AreaCode.objects.all().filter(organisation=user.organisation, **kwargs)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return AreaCodeCreationSerialiser
        else:
            return AreaCodeSerialiser

    def valid_organisation(self, request, data):
        return request.user.organisation.code == data['organisation']

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
        serialiser = AreaCodeSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.responses.DELETION_SUCCESS