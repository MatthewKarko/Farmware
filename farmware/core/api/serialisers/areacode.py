from rest_framework import serializers
from ..models.areacode import AreaCode

class AreaCodeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = AreaCode
        fields = '__all__'