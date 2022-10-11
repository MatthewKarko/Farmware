from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, exceptions
from rest_framework.fields import empty

from .models import User
from ..api.constants import ORG_CODE_LENGTH
from ..api.models.organisation import Organisation


class UserSerialiser(serializers.ModelSerializer):
    """Serialiser for the User model."""
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name', 'last_name', 'password', 
            'organisation', 'role', 'teams'
        ]
        read_only_field = ['created', 'updated']
        extra_kwargs = {'password': {'write_only': True}}


class UserUpdateSerialiser(UserSerialiser):
    """Serialiser for the User model."""
    class Meta(UserSerialiser.Meta):
        fields = UserSerialiser.Meta.fields
        fields.remove('organisation')
        fields.remove('password')

    def __init__(self, instance=None, data=empty, **kwargs):
        if instance is not None:
            print(instance.role, type(instance.role))
            print(User.Roles.choices)
            self.role = serializers.ChoiceField(
                choices=filter(lambda x: x[0] > instance.role, User.Roles.choices)
            )

        super().__init__(instance, data, **kwargs)

    def validate_role(self, value):
        if type(value) == str:
            try:
                value = User.Roles.labels.index(value)
            except ValueError:
                raise serializers.ValidationError("Role is not an option.")

        if value not in self.role.choices:
            raise serializers.ValidationError("Illegal role allocation.")

        return value


class LoginSerialiser(UserSerialiser):
    """Log in serialiser. Used to log a user in."""
    email = serializers.EmailField()

    class Meta(UserSerialiser.Meta):
        fields = ['email', 'password']


class RegisterSerialiser(UserSerialiser):
    """Registration Serialiser for admins."""
    org_name = serializers.CharField(required=True, write_only=True)

    class Meta(UserSerialiser.Meta):
        fields = [
            'first_name', 'last_name', 'password', 'email', 
        ]
        read_only_field = ['id']


class RegisterAdminSerialiser(RegisterSerialiser):
    """Registration Serialiser for admins."""
    org_name = serializers.CharField(required=True, write_only=True)

    class Meta(RegisterSerialiser.Meta):
        fields = RegisterSerialiser.Meta.fields + ['org_name']

    def create(self, validated_data):
        """Create an Admin."""
        # Create new organisation with a given org name
        organisation = Organisation(name=validated_data['org_name'])
        organisation.save()

        # Create a user—see if the user exists first.
        try:
            user = User.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            user = User.objects.create_admin(
                email=validated_data['email'], 
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                organisation=organisation, 
                password=validated_data['password']
            )
        return user


class RegisterUserSerialiser(RegisterSerialiser):
    """Registration serialiser for normal users."""
    org_code = serializers.CharField(max_length=ORG_CODE_LENGTH, write_only=True)

    class Meta(RegisterSerialiser.Meta):
        fields = RegisterSerialiser.Meta.fields + ['org_code']

    def create(self, validated_data):
        """Create a user."""
        # Try get the organisation.
        try:
            organisation = Organisation.objects.get(code=validated_data['org_code'])
        except Organisation.DoesNotExist:
            raise exceptions.NotAcceptable('Organisation code does not exist.')

        try:
            user = User.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            user = User.objects.create_user(
                email=validated_data['email'], 
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                organisation=organisation,
                password=validated_data['password'])
        return user

class PasswordSerialiser(serializers.Serializer):
    """Password serialiser."""
    # model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)