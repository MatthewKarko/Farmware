from django.http import QueryDict

from rest_framework import status, mixins, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

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

# class UserViewSet(ModelViewSet):
class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
    ):
    """User View Set."""
    serializer_class = UserSerialiser
    queryset = User.objects.all()

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this viewset 
        requires."""

        # Not instantiated
        if self.action is None: return []

        # Registration
        if 'register' in self.action: return [AllowAny()]

        # All others
        permission_classes = [IsAuthenticated, IsInOrganisation]

        # Updating or deleting information
        if ('update' in self.action) or (self.action == 'delete'):
            permission_classes.append(UserHierarchy)

        return [permission() for permission in permission_classes]

    def get_queryset(self, **kwargs):
        """Get the query set."""
        user: User = self.request.user
        return User.objects.all().filter(
            organisation=user.organisation,
            **kwargs
            )
    
    def get_serializer_class(self):
        """Get the serialiser class for the appropriate action."""
        if self.action == 'register_admin': return RegisterAdminSerialiser
        if self.action == 'register_user': return RegisterUserSerialiser
        return super().get_serializer_class()

    @action(detail=False, methods=['post'], url_path='register/admin')
    def register_admin(self, request):
        return self.create_user(request)

    @action(detail=False, methods=['post'], url_path='register/user')
    def register_user(self, request):
        return self.create_user(request)

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

    def create_user(self, request):
        """Create a new user."""
        data: QueryDict = request.data

        serliaser = self.get_serializer_class()(data=data)

        if serliaser.is_valid():
            user: User = serliaser.save()
            if user:
                # TODO: send confirmation email
                return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)

        return Response(serliaser.errors, status=status.HTTP_400_BAD_REQUEST)

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