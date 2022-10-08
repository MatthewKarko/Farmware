from rest_framework import serializers
from ..models.supplier import Supplier

class SupplierSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'phone_number']