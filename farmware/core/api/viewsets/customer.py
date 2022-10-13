from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ...user.models import User
from ...user.permissions import IsInOrganisation
from ..models import Customer
from ..serialisers import CustomerSerialiser

class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    RESPONSE_FORBIDDEN = Response({'error': 'You are not an admin of the specified organisation.'}, status=status.HTTP_403_FORBIDDEN)
    RESPONSE_CREATION_SUCCESS = Response({'success': 'Customer created.'}, status=status.HTTP_200_OK)
    RESPONSE_DELETION_SUCCESS = Response({'success': 'Customer deleted.'}, status=status.HTTP_200_OK)

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return Customer.objects.all().filter(organisation=user.organisation, **kwargs)

    def valid_organisation(self, request, data):
        return request.user.organisation.code == data['organisation']

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data
        if not self.valid_organisation(request, data):
            return self.RESPONSE_FORBIDDEN
        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)
        serialiser.save()
        return self.RESPONSE_CREATION_SUCCESS

    def update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        if not self.valid_organisation(request, data):
            return self.RESPONSE_FORBIDDEN
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = CustomerSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.RESPONSE_DELETION_SUCCESS