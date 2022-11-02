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
# 0001_initial,0002_initial,0003_auto_20221018_0824,0004_auto_20221018_1055,0005_auto_20221018_1132
from .urls import *
from django_test_migrations.contrib.unittest_case import MigratorTestCase
from django.test import Client
from rest_framework.test import APITestCase


class StockTestCases(TestCase):
    def setUp(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmon", logo="oat")
        organisatio = Organisation.objects.get(name="Farmon")
        produce = Produce.objects.create(organisation=organisatio, name="eggs")
        producequantitysuffix = ProduceQuantitySuffix.objects.create(
            produce_id=produce, suffix="lorem ipsum", base_equivalent=5.0)
        producevariety = ProduceVariety.objects.create(
            produce_id=produce, variety="brown")
        supplier = Supplier.objects.create(
            organisation=organisatio, name="john", phone_number="1234567891")
        areacode = AreaCode.objects.create(
            organisation=organisatio, area_code="204", description="just another area code")
        Stock.objects.create(organisation=organisatio, produce_id=produce,
                             variety_id=producevariety,
                             quantity=6.0,
                             quantity_suffix_id=producequantitysuffix,
                             supplier_id=supplier,
                             date_seeded="2022-10-25",
                             date_planted="2022-10-26",
                             date_picked="2022-10-27",
                             ehd="2022-10-28",
                             date_completed="2022-10-29",
                             area_code_id=areacode)

    def test_Stock1(self):
        stock = Stock.objects.get(quantity=6.0)
        # d=new Date("2022-10-28")
        # self.assertEqual(stock.ehd,d)
