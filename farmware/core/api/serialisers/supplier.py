from rest_framework import serializers
from ..models.supplier import Supplier

class SupplierSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class SupplierCreationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'phone_number']

    def create(self, validated_data):        
        # Add organisational data
        validated_data['organisation'] = self.context['request'].user.organisation
        return Supplier.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['organisation'] = self.context['request'].user.organisation
        return super().update(instance=instance, validated_data=validated_data)