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

class TeamViewsetTestCases(APITestCase):
    def test_create(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res=self.client.post('/api/team/',{'category':"Bananas",'name':"BananaCrazy"})
        self.assertEquals(res.status_code,200)
        res = self.client.get('/api/team/')
        res = res.json()
        self.assertEquals(len(res),1)
    def test_delete(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res=self.client.post('/api/team/',{'category':"Bananas",'name':"BananaCrazy"})
        self.assertEquals(res.status_code,200)
        res = self.client.get('/api/team/')
        res = res.json()
        team_id = res[0]['id']
        res=self.client.delete(f'/api/team/{team_id}/')
        self.assertEquals(res.status_code,200)
        res = self.client.get('/api/team/')
        res = res.json()
        self.assertEquals(len(res),0)
    def test_read(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res=self.client.post('/api/team/',{'category':"Bananas",'name':"BananaCrazy"})
        self.assertEquals(res.status_code,200)
        res = self.client.get('/api/team/')
        res = res.json()
        team_id = res[0]['id']
        res = self.client.get(f'/api/team/{team_id}/')
        res = res.json()
        self.assertEquals(res, {'category': 'Bananas', 'name': 'BananaCrazy'})
    def test_update_1(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res=self.client.post('/api/team/',{'category':"Bananas",'name':"BananaCrazy"})
        self.assertEquals(res.status_code,200)
        res = self.client.get('/api/team/')
        res = res.json()
        team_id = res[0]['id']
        res = self.client.put(f'/api/team/{team_id}/', {'category': 'Oranges', 'name': 'BananaCrazy'})
        self.assertEquals(res.status_code, 200)
    def test_update_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res=self.client.post('/api/team/',{'category':"Bananas",'name':"BananaCrazy"})
        self.assertEquals(res.status_code,200)
        res = self.client.get('/api/team/')
        res = res.json()
        team_id = res[0]['id']
        res = self.client.put(f'/api/team/{team_id}/', {'category': 'Oranges'})
        self.assertEquals(res.status_code, 200)
    def test_partial_update_1(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res=self.client.post('/api/team/',{'category':"Bananas",'name':"BananaCrazy"})
        self.assertEquals(res.status_code,200)
        res = self.client.get('/api/team/')
        res = res.json()
        team_id = res[0]['id']
        res = self.client.patch(f'/api/team/{team_id}/', {})
        self.assertEquals(res.status_code, 200)
        res = res.json()
        self.assertEquals(res, {'category': 'Bananas', 'name': 'BananaCrazy'})
    def test_partial_update_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res=self.client.post('/api/team/',{'category':"Bananas",'name':"BananaCrazy"})
        self.assertEquals(res.status_code,200)
        res = self.client.get('/api/team/')
        res = res.json()
        team_id = res[0]['id']
        res = self.client.patch(f'/api/team/{team_id}/', {'category': 'Oranges'})
        self.assertEquals(res.status_code, 200)
        res = res.json()
        self.assertEquals(res, {'category': 'Oranges', 'name': 'BananaCrazy'})
    def test_partial_update_3(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res=self.client.post('/api/team/',{'category':"Bananas",'name':"BananaCrazy"})
        self.assertEquals(res.status_code,200)
        res = self.client.get('/api/team/')
        res = res.json()
        team_id = res[0]['id']
        res = self.client.put(f'/api/team/{team_id}/', {'category': 'Oranges', 'name': 'OrangeCrazy'})
        self.assertEquals(res.status_code, 200)
        res = res.json()
        self.assertEquals(res, {'category': 'Oranges', 'name': 'OrangeCrazy'})
    
