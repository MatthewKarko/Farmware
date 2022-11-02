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
from .urls import *
from django_test_migrations.contrib.unittest_case import MigratorTestCase
from django.test import Client
from rest_framework.test import APITestCase


class ProduceViewsetTestCases(APITestCase):
    def setUp(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmone", logo="goat")
        organisatio = Organisation.objects.get(name="Farmone")
        produce = Produce.objects.create(organisation=organisatio, name="eggs")
        producequantitysuffix = ProduceQuantitySuffix.objects.create(
            produce_id=produce, suffix="lorem ipsum", base_equivalent=5.0)
        producevariety = ProduceVariety.objects.create(
            produce_id=produce, variety="brown")

    def test_creating(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_superuser(email="email@gmail.com",
                                                         first_name="first_name", last_name="last_name", password=None)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/api/produce/', {'organisation': organisatio, 'name': "eggs"})
        self.assertEquals(response.status_code, 200)

    def test_destroying(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_superuser(email="email@gmail.com",
                                                         first_name="first_name", last_name="last_name", password=None)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/api/produce/', {'organisation': organisatio, 'name': "eggs"})
        self.assertEquals(response.status_code, 200)
        response2 = self.client.delete(f'/api/produce/{user.pk}/')
        # print(response2.content)
        self.assertEquals(response2.status_code, 200)

    def test_partial_update(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_superuser(email="email@gmail.com",
                                                         first_name="first_name", last_name="last_name", password=None)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/api/produce/', {'organisation': organisatio, 'name': "eggs"})
        self.assertEquals(response.status_code, 200)
        response = self.client.patch(
            f'/api/produce/{user.pk}/', {'name': 'apple'})
        # print(response.content)
        self.assertEquals(response.status_code, 200)

    def test_update(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_superuser(email="email@gmail.com",
                                                         first_name="first_name", last_name="last_name", password=None)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/api/produce/', {'organisation': organisatio, 'name': "eggs"})
        self.assertEquals(response.status_code, 200)
        response = self.client.put(
            f'/api/produce/{user.pk}/', {'organisation': organisatio, 'name': "egs"})
        self.assertEquals(response.status_code, 200)

    def test_list(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_superuser(email="email@gmail.com",
                                                         first_name="first_name", last_name="last_name", password=None)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/api/produce/', {'organisation': organisatio, 'name': "eggs"})
        self.assertEquals(response.status_code, 200)
        response2 = self.client.get('/api/produce/')
        res = response.json()
        self.assertEquals(res[0]['name'], "eggs")
