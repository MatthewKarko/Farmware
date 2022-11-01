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

class CustomerViewsetTestCases(APITestCase):
    def setUp(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code =org_code,name="Farmone",logo="goat")
    def test_creating(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        response=self.client.post('/api/customer/',{'organisation':organisatio,'name':'ralph','phone_number':'9170002894'})
        self.assertEquals(response.status_code,200)
    def test_create_again(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        response=self.client.post('/api/customer/',{'organisation':organisatio,'name':'ralph','phone_number':'9170002894'})
        self.assertEquals(response.status_code,200)
        response2=self.client.post('/api/customer/',{'organisation':organisatio,'name':'ralph','phone_number':'9170002894'})
        self.assertEquals(response2.status_code,200)
    def test_destroy(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        response=self.client.post('/api/customer/',{'organisation':organisatio,'name':'ralph','phone_number':'9170002894'})
        self.assertEquals(response.status_code,200)
        response2=self.client.delete(f'/api/customer/{user.pk}/')
        self.assertEquals(response2.status_code,200)
    def test_partial_update(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        response=self.client.post('/api/customer/',{'organisation':organisatio,'name':'ralph','phone_number':'9170002894'})
        self.assertEquals(response.status_code,200)
        #getting pk from the viewset
        response2=self.client.patch(f'/api/customer/{user.pk}/',{'name':'ronnie'})
        self.assertEquals(response2.status_code,200)
    def test_update(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        response=self.client.post('/api/customer/',{'organisation':organisatio,'name':'ralph','phone_number':'9170002894'})
        self.assertEquals(response.status_code,200)
        org_code=generate_random_org_code()
        Organisation.objects.create(code =org_code,name="Farmtwo",logo="sheep")
        organisatio2=Organisation.objects.get(name="Farmtwo")
        response2=self.client.put(f'/api/customer/{user.pk}/',{'organisation':organisatio2,'name':'regal','phone_number':'9170002895'})
        self.assertEquals(response2.status_code,200)
    def test_list(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        response=self.client.post('/api/customer/',{'organisation':organisatio,'name':'ralph','phone_number':'9170002894'})
        self.assertEquals(response.status_code,200)
        response2=self.client.get('/api/customer/')
        res=response2.json()
        self.assertEquals(res[0]['name'],"ralph")
        self.assertTrue(response2.content)