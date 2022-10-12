from rest_framework import serializers
from ..models.areacode import AreaCode

class AreaCodeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = AreaCode
        fields = '__all__'
        verbose_name = "Area Code"
        verbose_name_plural = "Area Codes"