from django.test import TestCase
from django.contrib.auth import get_user_model
from .models.organisation import *
from .models.team import *
from .models.areacode import *
from .models.produce import *
from .models.stock import *
from .models.supplier import *
from .models.customer import *
from .models.order import *
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django_test_migrations.migrator import Migrator
from django.db import migrations, models
from core.api.migrations import *
from .urls import * #0001_initial,0002_initial,0003_auto_20221018_0824,0004_auto_20221018_1055,0005_auto_20221018_1132
from django_test_migrations.contrib.unittest_case import MigratorTestCase
from django.test import Client
from rest_framework.test import APITestCase

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
        with self.assertRaises(ValidationError):
            ProduceQuantitySuffix.objects.create(produce_id=produce2,suffix="ipsumLorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur cursus lectus id est dignissim dapibus. Integer mollis sodales urna, quis consectetur enim aliquam neself.client. Fusce nec velit nec lacus sollicitudin bibendum a ut augue. Fusce commodo lacus vel enim vulputate finibus. Integer aliquam quam at lorem imperdiet dignissim. Suspendisse volutpat.",base_equivalent=5.0)
            raise ValidationError("error")
