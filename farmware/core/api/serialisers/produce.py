from rest_framework import serializers
from ..models.produce import Produce
from ..models.produce import ProduceVariety
from ..models.produce import ProduceQuantitySuffix

class ProduceSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = '__all__'

    def create(self, validated_data):
        return Produce.objects.create(**validated_data)

class ProduceVarietySerialiser(serializers.ModelSerializer):
    class Meta:
        model = ProduceVariety
        fields = '__all__'
    
    def create(self, validated_data):
        return ProduceVariety.objects.create(**validated_data)

class ProduceQuantitySuffixSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ProduceQuantitySuffix
        fields = '__all__'
    
    def create(self, validated_data):
        return ProduceQuantitySuffix.objects.create(**validated_data)