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
class ProduceVarietyViewsetTestCases(APITestCase):
    def test_create(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        response=self.client.post('/api/produce_variety/',{'produce_id':produce_id,'variety':"brown"})
        self.assertEquals(response.status_code,200)
    def test_create_fail_1(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        response=self.client.post('/api/produce_variety/',{'produce_id': 4500,'variety':"brown"})
        self.assertEquals(response.status_code,400)
    def test_create_fail_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        response=self.client.post('/api/produce_variety/',{'produce_id':produce_id})
        self.assertEquals(response.status_code,400)
    def test_create_fail_3(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        response=self.client.post('/api/produce_variety/',{'produce_id':1,'variety':"brown"})
        self.assertEquals(response.status_code,400)
    def test_delete(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        response=self.client.post('/api/produce_variety/',{'produce_id':produce_id,'variety':"Tropical"})
        variety_id = response.json()['id']
        self.assertEquals(response.status_code,200)
        response=self.client.delete(f'/api/produce_variety/{variety_id}/')
        self.assertEquals(response.status_code,200)
    def test_partial_update(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        response=self.client.post('/api/produce_variety/',{'produce_id':produce_id,'variety':"brown"})
        self.assertEquals(response.status_code,200)
        variety_id = response.json()['id']
        response=self.client.patch(f'/api/produce_variety/{variety_id}/',{'variety':"green"})
        self.assertEquals(response.status_code,200)
    def test_get_variety(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        res=self.client.post('/api/produce_variety/',{'produce_id':produce_id,'variety':"Blood"})
        variety_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        res = self.client.get(f'/api/produce_variety/{variety_id}/')
        self.assertEquals(res.status_code,200)
    def test_get_variety_fail_1(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        res=self.client.post('/api/produce_variety/',{'produce_id':produce_id,'variety':"Blood"})
        variety_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        res = self.client.get(f'/api/produce_variety/{variety_id+1}/')
        self.assertEquals(res.status_code,404)
    def test_get_variet_fail_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.get(f'/api/produce_variety/{1}/')
        self.assertEquals(res.status_code,404)
    def test_list(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        response=self.client.post('/api/produce_variety/',{'produce_id':produce_id,'variety':"brown"})
        self.assertEquals(response.status_code,200)
        response2=self.client.get('/api/produce_variety/')
        res=response2.json()
        self.assertEquals(res[0]['variety'],"brown")
