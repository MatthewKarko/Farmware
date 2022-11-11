from django.test import TestCase
from ..models import *
from django.core.exceptions import ValidationError

class ProduceQuantitySuffixTestCases(TestCase):
    def setUp(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code =org_code,name="Farmon",logo="oat")
        organisatio=Organisation.objects.get(name="Farmon")
        produce=Produce.objects.create(organisation=organisatio,name="eggs")
        ProduceQuantitySuffix.objects.create(produce_id=produce,suffix="lorem ipsum",base_equivalent=5.0)
        
    def test_ProduceQuantitySuffix(self):
        producequantitysuffix=ProduceQuantitySuffix.objects.get(suffix="lorem ipsum")
        self.assertEqual(producequantitysuffix.base_equivalent,5.0)
        org_code=generate_random_org_code()
        Organisation.objects.create(code =org_code,name="Farmo",logo="oat")
        organisatio=Organisation.objects.get(name="Farmo")
        produce2=Produce.objects.create(organisation=organisatio,name="eggs")
        self.assertEquals(ProduceQuantitySuffix.objects.get(suffix="lorem ipsum").base_equivalent,5.0)
