from rest_framework import serializers
from ..models.produce import Produce
from ..models.produce import ProduceVariety
from ..models.produce import ProduceQuantitySuffix


### PRODUCE ###################################################################
class ProduceSerialiser(serializers.ModelSerializer):
    """Serialiser: Produce."""
    class Meta:
        model = Produce
        fields = ['id', 'name']

    def create(self, validated_data):
        return Produce.objects.create(**validated_data)


class ProduceCreationSerialiser(serializers.ModelSerializer):
    """Serialiser: Produce Creation."""
    class Meta:
        model = Produce
        fields = ['name']
    
    def create(self, validated_data):        
        # Add organisational data
        validated_data['organisation'] = self.\
            context['request'].user.organisation
        
        return Produce.objects.create(**validated_data)

class ProduceFullSerialiser(serializers.ModelSerializer):
    """Serialiser: Produce.
    Full information provided; this includes varieties and quantity suffixes.
    """
    class Meta:
        model = Produce
        fields = ['id', 'name']

    def to_representation(self, data):
        data = super(ProduceFullSerialiser, self).to_representation(data)
        data['varieties'] = ProduceVarietyInOrganisationSerialiser(
            ProduceVariety.objects.all().filter(produce_id=data.get('id')), 
            many=True
            ).data
        data['quantity_suffixes'] = ProduceQuantitySuffixInOrganisationSerialiser(
            ProduceQuantitySuffix.objects.all().filter(produce_id=data.get('id')), 
            many=True
            ).data
        return data
###############################################################################


### PRODUCE VARIETY ###########################################################
class ProduceVarietySerialiser(serializers.ModelSerializer):
    """Serialiser: Produce Variety."""
    class Meta:
        model = ProduceVariety
        fields = '__all__'


class ProduceVarietyInOrganisationSerialiser(serializers.ModelSerializer):
    """Serialiser: Produce Variety."""
    class Meta:
        model = ProduceVariety
        fields = ['id', 'variety']
###############################################################################


### PRODUCE QUANTITY SUFFIX ###################################################
class ProduceQuantitySuffixSerialiser(serializers.ModelSerializer):
    """Serialiser: Produce Quantity Suffix."""
    class Meta:
        model = ProduceQuantitySuffix
        fields = '__all__'


class ProduceQuantitySuffixInOrganisationSerialiser(serializers.ModelSerializer):
    """Serialiser: Produce Quantity Suffix."""
    class Meta:
        model = ProduceQuantitySuffix
        fields = ['id', 'suffix', 'base_equivalent']
###############################################################################