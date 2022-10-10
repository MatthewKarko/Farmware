from django.http import QueryDict

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .permissions import IsInOrganisation, UserHierarchy
from .serialisers import (
    RegisterUserSerialiser, 
    RegisterAdminSerialiser, 
    UserSerialiser, 
    UserUpdateSerialiser
)


TRUE = 'TRUE'
FALSE = 'FALSE'

class UserViewSet(ModelViewSet):
    """User View Set."""
    serializer_class = UserSerialiser
    queryset = User.objects.all()

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return User.objects.all().filter(
            organisation=user.organisation,
            **kwargs
            )

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this viewset 
        requires."""
        if self.action == 'create': return [AllowAny]

        permission_classes = [IsAuthenticated, IsInOrganisation]

        if ('update' in self.action) or (self.action == 'delete'):
            permission_classes.append(UserHierarchy)

        return [permission() for permission in permission_classes]

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
        """Update a user's information."""
        # Data and user
        data: QueryDict = request.data
        user: User = self.request.user

        # Serialiser
        serialiser = UserUpdateSerialiser(
            instance=user, 
            data=data, 
            partial=True)
        serialiser.is_valid(raise_exception=True)

        return super().partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """List all users in one's organisation."""
        serialiser = self.get_serializer(
            instance=self.get_queryset(), many=True
            )
        return Response(serialiser.data)

    # @action(detail=True, methods=['post'])
    # def set_password(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = PasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user.set_password(serializer.validated_data['password'])
    #         user.save()
    #         return Response({'status': 'password set'})
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)