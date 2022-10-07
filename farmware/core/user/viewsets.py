from django.db import IntegrityError
from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .permissions import IsInOrganisation
from .models import User
from .serialisers import RegisterUserSerialiser, RegisterAdminSerialiser, UserSerialiser

TRUE = 'TRUE'
FALSE = 'FALSE'


class UserViewSet(ModelViewSet):
    """User View Set"""
    serializer_class = UserSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    queryset = User.objects.all()

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return User.objects.all().filter(
            organisation=user.organisation,
            **kwargs
            )

    # def get_object(self):
    #     lookup_field_value = self.kwargs[self.lookup_field]

    #     obj = User.objects.get(lookup_field_value)
    #     self.check_object_permissions(self.request, obj)

    #     return obj

    def create(self, request, *args, **kwargs):
        """Create a new user."""
        data: QueryDict = request.data

        # See if a new organisation is trying to be made
        if data.get('new_org', FALSE).upper() == TRUE:
            serializer = RegisterAdminSerialiser(data=data)
        else:
            serializer = RegisterUserSerialiser(data=data)

        if serializer.is_valid():
            user: User = serializer.save()
            if user:
                # TODO: send confirmation email
                return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        serialiser = self.get_serializer(self.get_queryset(), many=True)
        return Response(serialiser.data)