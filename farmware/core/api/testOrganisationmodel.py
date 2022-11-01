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

class OrganisationTestCases(TestCase):
    def setUp(self):
        Organisation.objects.create(name="Farmone",logo="goat")
        Organisation.objects.create(name="Farmtwo",logo="sheep")
    def test_organisation_(self):
        farmone = Organisation.objects.get(name="Farmone")
        farmtwo = Organisation.objects.get(name="Farmtwo")
        self.assertEqual(farmone.name, "Farmone")
        self.assertEqual(farmone.logo, "goat")
        self.assertEqual(farmtwo.name, "Farmtwo")
        self.assertEqual(farmtwo.logo, "sheep")
    def test_organisation2(self):
        with self.assertRaises(Exception):
            self.assertRaises(Organisation.objects.create(name=4,logo="sheep"))
    def test_organisation3(self):
        with self.assertRaises(ValidationError):
            Organisation.objects.create(name="anotherna",logo=5.0)
            raise ValidationError("error")
    def test_organisation4(self):
        with self.assertRaises(ValidationError):
            Organisation.objects.create(name="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas commodo cursus condimentum. Donec pulvinar odio sed enim tristique, sit amet tristique dolor volutpat. Proin nec mauris gravida libero scelerisque consectetur non at sapien. Nam et felis nibh. Morbi eget augue sit amet nisl elementum congue. Nulla vel laoreet velit. Nullam est neque, efficitur sodales suscipit ac, vulputate eget velit. Doneself.client.",logo="i")
            raise ValidationError("Error")
    def test_organisation5(self):
        with self.assertRaises(ValidationError):
            Organisation.objects.create(name="a",logo="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas commodo cursus condimentum. Donec pulvinar odio sed enim tristique, sit amet tristique dolor volutpat. Proin nec mauris gravida libero scelerisque consectetur non at sapien. Nam et felis nibh. Morbi eget augue sit amet nisl elementum congue. Nulla vel laoreet velit. Nullam est neque, efficitur sodales suscipit ac, vulputate eget velit. Doneself.client.")
            raise ValidationError("error")
