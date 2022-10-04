# from rest_framework import serializers, exceptions

# from django.core.exceptions import ObjectDoesNotExist

# from ..user.serialisers import UserSerialiser, AdminSerialiser
# from ..user.models import User
# from ..api.models.organisation import Organisation
# from ..api.constants import ORG_CODE_LENGTH


# class LoginSerialiser(UserSerialiser):
#     """Log in serialiser. Used to log a user in."""
#     email = serializers.EmailField()

#     class Meta:
#         model = User
#         fields = ['email', 'password']


# class RegisterAdminSerialiser(AdminSerialiser):
#     """Registration Serialiser for Admins."""
#     org_name = serializers.CharField(required=False, write_only=True)
#     first_name = serializers.CharField(required=False)

#     class Meta:
#         model = User
#         fields = [
#             'id',
#             'first_name', 'last_name', 'password', 'email', 'username', 
#             'org_name'
#         ]
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         """Create an Admin."""
#         # Create new organisation with a given org name
#         organisation = Organisation(name=validated_data['org_name'])
#         organisation.save()

#         print('validated_data:', validated_data)

#         # Create a user—see if the user exists first.
#         try:
#             user = User.objects.get(email=validated_data['email'])
#         except ObjectDoesNotExist:
#             user = User.objects.create_user(
#                 email=validated_data['email'], 
#                 first_name=validated_data['first_name'],
#                 last_name=validated_data['last_name'],
#                 organisation=organisation, 
#                 password=validated_data['password'])
#         return user


# class RegisterUserSerialiser(UserSerialiser):
#     """Registration Serialiser for normal Users."""
#     org_code = serializers.CharField(max_length=ORG_CODE_LENGTH, write_only=True)

#     class Meta:
#         model = User
#         fields = [
#             'id',
#             'first_name', 'last_name', 'password', 'email', 
#             'org_code'
#         ]

#     def create(self, validated_data):
#         """Create a user."""
#         # Try get the organisation.
#         try:
#             organisation = Organisation.objects.get(code=validated_data['org_code'])
#         except Organisation.DoesNotExist:
#             raise exceptions.NotAcceptable('Organisation code does not exist.')

#         try:
#             user = User.objects.get(email=validated_data['email'])
#         except ObjectDoesNotExist:
#             user = User.objects.create_user(
#                 email=validated_data['email'], 
#                 first_name=validated_data['first_name'],
#                 last_name=validated_data['last_name'],
#                 organisation=organisation,
#                 password=validated_data['password'],
#                 **self.data)
#         return user