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
    def test_create(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        response=self.client.post('/api/produce/',{'name':"Mangoes"})
        self.assertEquals(response.status_code,200)
    def test_create_fail_1(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        response=self.client.post('/api/produce/',{})
        self.assertEquals(response.status_code,400)
    def test_read(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        response=self.client.post('/api/produce/',{'name':"Mangoes"})
        produce_id = list(response.data.values())[0]
        self.assertEquals(response.status_code,200)
        response=self.client.get(f'/api/produce/{produce_id}/')
        self.assertEquals(response.status_code,200)
    def test_read(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        response=self.client.post('/api/produce/',{'name':"Mangoes"})
        produce_id = list(response.data.values())[0]
        self.assertEquals(response.status_code,200)
        response=self.client.get(f'/api/produce/{produce_id}/')
        self.assertEquals(response.status_code,200)
        response=self.client.get(f'/api/produce/{produce_id}/')
        self.assertEquals(response.status_code,200)
    def test_read_fail_1(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        response=self.client.post('/api/produce/',{'name':"Mangoes"})
        produce_id = list(response.data.values())[0]
        self.assertEquals(response.status_code,200)
        response=self.client.get(f'/api/produce/{produce_id+1}/')
        self.assertEquals(response.status_code,404)
    def test_read_fail_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        response=self.client.post('/api/produce/',{'name':"Mangoes"})
        produce_id = list(response.data.values())[0]
        self.assertEquals(response.status_code,200)
        response=self.client.get(f'/api/produce/{produce_id}/')
        self.assertEquals(response.status_code,200)
        self.client.delete(f'/api/produce/{produce_id}/')
        response=self.client.get(f'/api/produce/{produce_id}/')
        self.assertEquals(response.status_code,404)
    def test_delete(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        res=self.client.delete(f'/api/produce/{produce_id}/')
        self.assertEquals(res.status_code,200)
    def test_delete_fail_1(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        res=self.client.delete(f'/api/produce/{produce_id+1}/')
        self.assertEquals(res.status_code,404)
    def test_delete_fail_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        res=self.client.delete(f'/api/produce/{produce_id}/')
        self.assertEquals(res.status_code,200)
        res=self.client.delete(f'/api/produce/{produce_id}/')
        self.assertEquals(res.status_code,404)
    def test_update_1(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        response=self.client.put(f'/api/produce/{produce_id}/',{'name':'Banana'})
        self.assertEquals(response.status_code,200)
    def test_update_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        response=self.client.put(f'/api/produce/{produce_id}/',{'name':'Banana'})
        self.assertEquals(response.status_code,200)
        response=self.client.put(f'/api/produce/{produce_id}/',{'name':'Orange'})
        self.assertEquals(response.status_code,200)
        response=self.client.put(f'/api/produce/{produce_id}/',{'name':'Grape'})
        self.assertEquals(response.status_code,200)
    def test_update_fail_1(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        response=self.client.put(f'/api/produce/{produce_id+1}/',{'name':'Banana'})
        self.assertEquals(response.status_code,400)
    def test_update_fail_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        response=self.client.put(f'/api/produce/{produce_id}/',{})
        self.assertEquals(response.status_code,400)
    def test_partial_update_1(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        response=self.client.patch(f'/api/produce/{produce_id}/',{'name':'Orange'})
        self.assertEquals(response.status_code,200)
    def test_partial_update_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        response=self.client.patch(f'/api/produce/{produce_id}/',{})
        self.assertEquals(response.status_code,200)
    def test_partial_update_fail(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        produce_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        response=self.client.patch(f'/api/produce/{produce_id+1}/',{})
        self.assertEquals(response.status_code,400)
    def test_create_varieties(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        response=self.client.post(f'/api/produce/{produce_id}/create_varieties/',{'name': "['Green', 'Red', 'Tropical']"})
        self.assertEquals(response.status_code,200)
    def test_get_suffixes(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"kgs",'base_equivalent':1.0})
        self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"grams",'base_equivalent':0.1})
        self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"tonnes",'base_equivalent':1000})
        res = self.client.get(f'/api/produce/{produce_id}/get_suffixes/')
        res = res.json()
        self.assertEquals(len(res), 3)
    def test_get_suffixes_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        res = self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"kgs",'base_equivalent':1.0})
        suffix_id = list(res.data.values())[0]
        self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"grams",'base_equivalent':0.1})
        self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"tonnes",'base_equivalent':1000})
        res = self.client.get(f'/api/produce/{produce_id}/get_suffixes/')
        res = res.json()
        self.assertEquals(len(res), 3)
        res = self.client.delete(f'/api/produce_quantity_suffix/{suffix_id}/')
        res = res.json()
        self.assertEquals(len(res), 1)
    def test_get_varieties(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        self.client.post(f'/api/produce/{produce_id}/create_varieties/',{'name': "['Green', 'Red', 'Tropical']"})
        res = self.client.get(f'/api/produce/{produce_id}/get_varieties/')
        res = res.json()
        self.assertEquals(len(res), 3)
    def test_get_varieties_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        res = self.client.post(f'/api/produce/{produce_id}/create_varieties/',{'name': "['Green', 'Red', 'Tropical']"})
        res = res.json()
        variety_id = res[0]['id']
        res = self.client.get(f'/api/produce/{produce_id}/get_varieties/')
        res = res.json()
        self.assertEquals(len(res), 3)
        res = self.client.delete(f'/api/produce_variety/{variety_id}/')
        res = self.client.get(f'/api/produce/{produce_id}/get_varieties/')
        res = res.json()
        self.assertEquals(len(res), 2)
    def test_list(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Pear'})
        self.assertEquals(res.status_code,200)
        res=self.client.get('/api/produce/')
        res=res.json()
        self.assertEquals(res[0]['name'],"Pear")
    def test_list_empty(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res=self.client.get('/api/produce/')
        res=res.json()
        self.assertEquals(len(res),0)
