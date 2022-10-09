from rest_framework import serializers
from ..models.produce import Produce
from ..models.produce import ProduceVariety
from ..models.produce import ProduceQuantitySuffix

class ProduceSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = '__all__'

class ProduceVarietySerialiser(serializers.ModelSerializer):
    class Meta:
        model = ProduceVariety
        fields = '__all__'

class ProduceQuantitySuffixSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ProduceQuantitySuffix
        fields = '__all__'