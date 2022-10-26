from rest_framework import serializers
from ..models.areacode import AreaCode

class AreaCodeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = AreaCode
        fields = '__all__'

class AreaCodeCreationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = AreaCode
        exclude = ['organisation']
    
    def create(self, validated_data):
        validated_data['organisation'] = self.context['request'].user.organisation
        return AreaCode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['organisation'] = self.context['request'].user.organisation
        return super().update(instance=instance, validated_data=validated_data)