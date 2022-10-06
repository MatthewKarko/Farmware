from django.conf import settings
from rest_framework import serializers

from .models.organisation import Organisation
from .models.team import Team
from ..user.models import User

class OrganisationSerialiser(serializers.ModelSerializer):
    organisation = serializers.ModelField(User, write_only=True)
    class Meta:
        model = Organisation
        fields = ('code', 'name', 'organisation')

class TeamCreationSerialiser(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True)
    class Meta:
        model = Team
        fields = ['category', 'name']

    def create(self, validated_data):
        # If name is not given, default to category name
        if validated_data['name'] == '': 
            validated_data['name'] = validated_data['category']
        
        # Add organisational data
        validated_data['organisation'] = self.\
            context['request'].user.organisation
        
        return Team.objects.create(**validated_data)

class TeamSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'