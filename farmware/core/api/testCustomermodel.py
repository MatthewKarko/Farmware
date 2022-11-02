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
class  CustomerTestCases(TestCase):
    def setUp(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code =org_code,name="Farmone",logo="goat")
        organisatio=Organisation.objects.get(name="Farmone")
        Customer.objects.create(organisation=organisatio,name = "Henry",phone_number="9191223445" )

    def test_Customer1(self):
        customer = Customer.objects.get(name = "Henry")
        self.assertEqual(customer.phone_number,"9191223445")
    def test_Customer2(self):
        customer = Customer.objects.get(name = "Henry")
        with self.assertRaises(IntegrityError):
            Customer.objects.create(name = "Henr",phone_number="91912234452" )
            raise IntegrityError("error")
    def test_Customer3(self):
        #customer = Customer.objects.get(name = "Henry")
        org_code=generate_random_org_code()
        Organisation.objects.create(code =org_code,name="Farmon",logo="oat")
        organisatio=Organisation.objects.get(name="Farmon")
        with self.assertRaises(ValidationError):
            Customer.objects.create(organisation=organisatio,name = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas commodo cursus condimentum. Donec pulvinar odio sed enim tristique, sit amet tristique dolor volutpat. Proin nec mauris gravida libero scelerisque consectetur non at sapien. Nam et felis nibh. Morbi eget augue sit amet nisl elementum congue. Nulla vel laoreet velit. Nullam est neque, efficitur sodales suscipit ac, vulputate eget velit. Doneself.client.",phone_number="9191223445")
            raise ValidationError("error")
