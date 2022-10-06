from django.conf import settings
from rest_framework import serializers
from ...user.models import User
from ..models.organisation import  Organisation

class OrganisationSerialiser(serializers.ModelSerializer):
    organisation = serializers.ModelField(User, write_only=True)
    class Meta:
        model = Organisation
        fields = ['code', 'name', 'organisation']