from core.user.models import User, Admin
from rest_framework import serializers


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'first_name', 'last_name', 'username', 'password', 'email', 
            'organisation', 'role', 'teams',
            'is_active'
        ]
        read_only_field = ['is_active', 'created', 'updated']

class AdminSerialiser(UserSerialiser):
    class Meta:
        model = Admin