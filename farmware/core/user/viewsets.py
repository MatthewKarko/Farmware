from django.db import IntegrityError
from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .permissions import IsInOrganisation
from .models import User
from .serialisers import RegisterUserSerialiser, RegisterAdminSerialiser, UserSerialiser, UserUpdateSerialiser

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

    def partial_update(self, request, *args, **kwargs):
        data: QueryDict = request.data
        user: User = self.request.user
        serializer = UserUpdateSerialiser(instance=user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        # User can not edit a ROLE, admin can.
        # if 'role' in data:
        #     if user.role < User.Roles.ORGANISATION_ADMIN: 
        #     if user.role < User.Roles.ADMIN:
        #         data.pop('role')
        #     else:
        #         if 
            # if user.role < User.Roles.ADMIN and 'role' in data:
            #     data.pop('role')

        return super().partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serialiser = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serialiser.data)