from rest_framework import serializers
from ..models.organisation import  Organisation

class OrganisationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'