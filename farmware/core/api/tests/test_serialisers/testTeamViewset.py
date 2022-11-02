from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models.organisation import *
from ...models.team import *
from ...models.areacode import *
from ...models.produce import *
from ...models.stock import *
from ...models.supplier import *
from ...models.customer import *
from ...models.order import *
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django_test_migrations.migrator import Migrator
from django.db import migrations, models
from core.api.migrations import *
# 0001_initial,0002_initial,0003_auto_20221018_0824,0004_auto_20221018_1055,0005_auto_20221018_1132
from ...urls import *
from django_test_migrations.contrib.unittest_case import MigratorTestCase
from django.test import Client
from rest_framework.test import APITestCase


class TeamViewsetTestCases(APITestCase):
    def setUp(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmone", logo="goat")
        organisatio = Organisation.objects.get(name="Farmone")

    def test_creating(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        self.client.force_authenticate(user)
        organisatio = Organisation.objects.get(name="Farmone")
        response = self.client.post(
            '/api/team/', {'category': "cricket", 'name': "number1", 'organisation': organisatio})
        self.assertEquals(response.status_code, 200)

    def test_destroying(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        self.client.force_authenticate(user)
        organisatio = Organisation.objects.get(name="Farmone")
        response = self.client.post(
            '/api/team/', {'category': "cricket", 'name': "number1", 'organisation': organisatio})
        self.assertEquals(response.status_code, 200)
        response = self.client.delete(f'/api/team/{user.pk}/')
        self.assertEquals(response.status_code, 200)

    def test_list(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        self.client.force_authenticate(user)
        organisatio = Organisation.objects.get(name="Farmone")
        response = self.client.post(
            '/api/team/', {'category': "cricket", 'name': "number1", 'organisation': organisatio})
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/api/team/')
        res = response.json()
        self.assertEquals(res[0]['category'], "cricket")
