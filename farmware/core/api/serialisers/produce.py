from rest_framework import serializers
from ..models.produce import Produce
from ..models.produce import ProduceVariety
from ..models.produce import ProduceQuantitySuffix

class ProduceSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = ['name']

class ProduceVarietySerialiser(serializers.ModelSerializer):
    class Meta:
        model = ProduceVariety
        fields = ['produce_id', 'variety']

class ProduceQuantitySuffixSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ProduceQuantitySuffix
        fields = ['produce_id', 'suffix', 'base_equivalent']