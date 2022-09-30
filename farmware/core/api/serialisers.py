from rest_framework import serializers

from .models.organisation import Organisation
from .models.team import Team

class OrganisationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('org_code', 'org_name')

class TeamSerialiser(serializers.ModelSerializer):
    # TODO: fix
    # Create a custom method field
    current_user = serializers.SerializerMethodField('_user')

    # Use this method for the custom field
    def _user(self, obj):
        request = self.context.get('request', None)
        if request: return request.user

    class Meta:
        model = Team
        fields = ('category', 'name')

    def create(self, validated_data):
        print('Team VD:', validated_data)
        # print('User:', self._user())

        return super().create(**validated_data)