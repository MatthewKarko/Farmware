from rest_framework import serializers
from ..models.customer import Customer

class CustomerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerCreationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number']

    def create(self, validated_data):        
        # Add organisational data
        validated_data['organisation'] = self.\
            context['request'].user.organisation

        print('CustomerCreationSerialiser create:', validated_data)
        
        return Customer.objects.create(**validated_data)