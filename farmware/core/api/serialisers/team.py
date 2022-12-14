from rest_framework import serializers
from ..models.team import Team


class TeamSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        
class TeamCreationSerialiser(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True, required=False)

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