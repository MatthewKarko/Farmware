from django.contrib.auth import get_user_model
from ..models import *
from rest_framework.test import APITestCase

class ProduceQuantitySuffixViewsetTestCases(APITestCase):
    def test_create(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        response=self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"lorem ipsum",'base_equivalent':5.0})
        self.assertEquals(response.status_code,200)

    def test_create_expectedfail(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Orange'})
        produce_id = list(res.data.values())[0]
        response=self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id, 'base_equivalent':5.0})
        self.assertEquals(response.status_code,400)

    def test_delete(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        response=self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"lorem ipsum",'base_equivalent':5.0})
        self.assertEquals(response.status_code,200)
        suffix_id = list(response.data.values())[0]
        response=self.client.delete(f'/api/produce_quantity_suffix/{suffix_id}/')
        self.assertEquals(response.status_code,200)

    def test_delete_expectedfail(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        response=self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"lorem ipsum",'base_equivalent':5.0})
        self.assertEquals(response.status_code,200)
        suffix_id = list(response.data.values())[0]
        response=self.client.delete(f'/api/produce_quantity_suffix/{5}/')
        self.assertEquals(response.status_code,404)

    def test_delete_expectedfail_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        response=self.client.delete(f'/api/produce_quantity_suffix/{1}/')
        self.assertEquals(response.status_code,404)

    def test_partial_update(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        response=self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"tonne",'base_equivalent':5.0})
        suffix_id = list(response.data.values())[0]
        self.assertEquals(response.status_code,200)
        response2=self.client.patch(f'/api/produce_quantity_suffix/{suffix_id}/',{'suffix':"kg"})
        self.assertEquals(response2.status_code,200)

    def test_get_qs(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        res=self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"lorem ipsum",'base_equivalent':5.0})
        suffix_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        res = self.client.get(f'/api/produce_quantity_suffix/{suffix_id}/')
        self.assertEquals(res.status_code,200)

    def test_get_qs_fail_1(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        res=self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"lorem ipsum",'base_equivalent':5.0})
        suffix_id = list(res.data.values())[0]
        self.assertEquals(res.status_code,200)
        res = self.client.get(f'/api/produce_quantity_suffix/{suffix_id+1}/')
        self.assertEquals(res.status_code,404)

    def test_get_qs_fail_2(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.get(f'/api/produce_quantity_suffix/{1}/')
        self.assertEquals(res.status_code,404)
        
    def test_list(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)
        res = self.client.post('/api/produce/', {'name': 'Apple'})
        produce_id = list(res.data.values())[0]
        res=self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"grams",'base_equivalent':5.0})
        self.assertEquals(res.status_code,200)
        response=self.client.get('/api/produce_quantity_suffix/')
        res=response.json()
        self.assertEquals(res[0]['suffix'],"grams")
        res=self.client.post('/api/produce_quantity_suffix/',{'produce_id':produce_id,'suffix':"kgs",'base_equivalent':1.0})
        response=self.client.get('/api/produce_quantity_suffix/')
        res=response.json()
        self.assertEquals(len(res), 2)
