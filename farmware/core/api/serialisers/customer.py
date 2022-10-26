from rest_framework import serializers
from ..models.customer import Customer

class CustomerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerCreationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['organisation']

    def create(self, validated_data):
        # Add organisational data
        validated_data['organisation'] = self.context['request'].user.organisation
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['organisation'] = self.context['request'].user.organisation
        return super().update(instance=instance, validated_data=validated_data)