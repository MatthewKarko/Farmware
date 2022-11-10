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

# Tests the Customer objects in model
class CustomerTestCases(TestCase):
    def setUp(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmone", logo="goat")
        organisatio = Organisation.objects.get(name="Farmone")
        Customer.objects.create(organisation=organisatio,
                                name="Henry", phone_number="9191223445")

    #Test that the created customer fields are set correctly.
    def test_Customer_fields(self):
        customer = Customer.objects.get(name="Henry")
        self.assertEqual(customer.phone_number, "9191223445")

    #Test that multiple customers can be added to the organisation
    def test_Customer_multiple(self):
        #customer = Customer.objects.get(name = "Henry")
        org = Organisation.objects.get(name="Farmone")
        Customer.objects.create(organisation=org, name="Billy Brown", phone_number="9119119123")
        Customer.objects.create(organisation=org, name="Sam Brown", phone_number="1233213211")
        Customer.objects.create(organisation=org, name="Xyz", phone_number="1231231231")

        customer = Customer.objects.get(name="Billy Brown")
        self.assertEqual(customer.phone_number, "9119119123")
        customer = Customer.objects.get(name="Sam Brown")
        self.assertEqual(customer.phone_number, "1233213211")
        customer = Customer.objects.get(name="Xyz")
        self.assertEqual(customer.phone_number, "1231231231")
