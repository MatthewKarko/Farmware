from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core import exceptions
from django.http import QueryDict
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from rest_framework import status, mixins, serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .permissions import IsInOrganisation, UserHierarchy, OnlyYou
from .serialisers import (
    RegisterUserSerialiser,
    RegisterAdminSerialiser,
    UserSerialiser,
    UserUpdateSerialiser,
    PasswordSerialiser
)
from .tokens import account_activation_token
from ..api.models.team import Team


TRUE = 'TRUE'
FALSE = 'FALSE'

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

        # Set Password
        if self.action == self.set_password.__name__:
            return [OnlyYou()]

        # All others
        permission_classes = [IsAuthenticated, IsInOrganisation]

        # Updating or deleting information
        if ('update' in self.action) or (self.action == 'destroy'):
            permission_classes.append(UserHierarchy)

        return [permission() for permission in permission_classes]


    def get_queryset(self, **kwargs):
        """Get the query set."""
        user: User = self.request.user  # type: ignore
        return User.objects.all().filter(
            organisation=user.organisation,
            **kwargs
            )

    def get_serializer_class(self):
        """Get the serialiser class for the appropriate action."""
        if self.action == 'register_admin': return RegisterAdminSerialiser
        if self.action == 'register_user': return RegisterUserSerialiser
        if self.action == 'set_password': return PasswordSerialiser

        if 'update' in self.action: return UserUpdateSerialiser

        return super().get_serializer_class()

    @action(detail=False, methods=['post'], url_path='register/admin')
    def register_admin(self, request):
        """Register as an admin, i.e., create a new organisation."""
        return self.create_user(request)

    @action(detail=False, methods=['post'], url_path='register/user')
    def register_user(self, request):
        """Register as a user."""
        return self.create_user(request)

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        """Set a new password for a user."""
        user: User = self.get_object()
        serialiser = self.get_serializer_class()(
            data=request.data
            )

        if str(user.id) != str(pk):  # type: ignore
            return Response(
                {'error': 'You do not have permission to do this.'},
                status=status.HTTP_400_BAD_REQUEST
                )

        if not serialiser.is_valid():
            return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)

        # Check old password
        if not user.check_password(serialiser.data.get("old_password")):  # type: ignore
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(serialiser.data.get("new_password"), user)  # type: ignore
        except exceptions.ValidationError as e:
            errors = []
            for error in e.error_list:
                message = error.message
                if error.params:
                    message %= error.params
                errors.append(str(message))

            raise serializers.ValidationError({'new_password': errors})

        user.set_password(serialiser.data.get("new_password"))
        user.save()
        return Response({'success': 'Password successfully updated.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='teams')
    def my_teams(self, request):
        """Get all the teams a user is a member of."""
        user: User = request.user

        teams = []

        team: Team
        for team in user.teams.all():
            fields = team.__dict__
            fields.pop('_state')
            fields.pop('organisation_id')
            teams.append(fields)

        return Response({'teams': teams}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='teams')
    def users_teams(self, request, pk=None):
        """Get all the teams a user is a member of."""
        user: User = self.get_object()

        teams = []

        team: Team
        for team in user.teams.all():
            fields = team.__dict__
            fields.pop('_state')
            fields.pop('organisation_id')
            teams.append(fields)

        return Response({'teams': teams}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """Update a user's information."""
        # Data and user
        data: QueryDict = request.data
        user: User = self.request.user  # type: ignore

        # Serialiser
        serialiser = self.get_serializer_class()(
            instance=user,
            data=data,   # type: ignore
            partial=True)
        serialiser.is_valid(raise_exception=True)

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Remove a user."""
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """List all users in one's organisation."""
        serialiser = self.get_serializer(
            instance=self.get_queryset(), many=True
            )
        return Response(serialiser.data)

    def create_user(self, request):
        """Create a new user."""
        data: QueryDict = request.data
        user: User = request.user
        try:
            validate_password(data['password'], user)
        except exceptions.ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        serialiser = self.get_serializer_class()(data=data)  # type: ignore
        if serialiser.is_valid():
            user: User = serialiser.save()
            if user:
                # TODO: activate send confirmation email
                # self.send_email_verification(request, user)
                return Response(status=status.HTTP_201_CREATED)

        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_email_verification(self, request, user: User) -> None:
        """Send an email verification to the given user."""
        current_site = get_current_site(request)
        mail_subject = 'Activate your blog account.'
        html_message = render_to_string('activate_account_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        plain_message = strip_tags(html_message)
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=plain_message,
            from_email=None,
            recipient_list=[to_email],
            html_message=html_message
        )
        # TODO: add verification / error checking
