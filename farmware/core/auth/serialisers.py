from rest_framework import serializers, exceptions

from django.core.exceptions import ObjectDoesNotExist

from ..user.serialisers import UserSerialiser, AdminSerialiser
from ..user.models import User, Admin
from ..api.models import Organisation
from ..api.constants import ORG_CODE_LENGTH


class LoginSerialiser(UserSerialiser):
    """Log in serialiser. Used to log a user in."""
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']


class RegisterAdminSerialiser(AdminSerialiser):
    """Registration Serialiser for Admins."""
    org_name = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = Admin
        fields = [
            'id',
            'first_name', 'last_name', 'password', 'email', 'username', 
            'org_name', 'is_active'
        ]

    def create(self, validated_data):
        """Create an Admin."""
        # Create new organisation with a given org name
        org = Organisation(org_name=self.data['org_name'])
        org.save()

        # Create a user—see if the user exists first.
        try:
            user = Admin.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            user = Admin.objects.create(organisation=org, **self.data)
        return user


class RegisterUserSerialiser(UserSerialiser):
    """Registration Serialiser for normal Users."""
    org_code = serializers.CharField(max_length=ORG_CODE_LENGTH, write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name', 'last_name', 'password', 'email', 'username', 
            'org_code', 'is_active'
        ]

    def create(self, validated_data):
        """Create a user."""
        # Try get the organisation.
        try:
            org = Organisation.objects.get(code=validated_data['org_code'])
        except Organisation.DoesNotExist:
            raise exceptions.NotAcceptable('Organisation code does not exist.')

        try:
            user = User.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            user = User.objects.create_user(organisation=org, **self.data)
        return user