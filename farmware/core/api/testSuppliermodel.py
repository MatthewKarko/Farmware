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


class SupplierTestCases(TestCase):
    def setUp(self):
        self.org_code = generate_random_org_code()
        self.org = Organisation.objects.create(code = self.org_code, name = "Org", logo="img")
        self.s_name = "Supplier"
        self.s_pn = "012456789"
        self.s = Supplier.objects.create(organisation=self.org, name = self.s_name, phone_number = self.s_pn)
        self.s2 = Supplier.objects.create(organisation=self.org, name = self.s_name+"2", phone_number = self.s_pn+"2")

    # Checking whether the supplier objects have been created correctly
    def test_SupplierFields(self):
        self.assertEquals(self.s.name, self.s_name)
        self.assertEquals(self.s.phone_number, self.s_pn)
        self.assertEquals(self.s2.name, self.s_name+"2")
        self.assertEquals(self.s2.phone_number, self.s_pn+"2")

    def test_SupplierCreationException(self):
        with self.assertRaises(ValueError):
            Supplier.objects.create(organisation=0, phone_number=self.s_pn)