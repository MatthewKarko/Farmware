from django.contrib.auth import get_user_model
from ..models import *
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

    # Test that the team endpoints are not accessible to an unauthorised user.
    def test_unauthorised_user(self):
        # Test create is inaccessible
        res=self.client.post('/api/team/',{'category':"Bananas",'name':"BananaCrazy"})
        self.assertEquals(res.status_code,401)

        # Test delete is inaccessible
        res_del=self.client.delete(f'/api/team/0/')
        self.assertEquals(res_del.status_code,401)

        # Test update is inaccessible
        res_update = self.client.put(f'/api/team/0/', {'category': 'Oranges'})
        self.assertEquals(res_update.status_code, 401)

        # Test patch in inaccessible
        res_patch = self.client.patch(f'/api/team/0/', {})
        self.assertEquals(res_patch.status_code, 401)

        # Test list in inaccessible
        res_get = self.client.get('/api/team/')
        self.assertEquals(res_get.status_code, 401)


    #Tests the field limits in Team model
    def test_field_validation(self):
        user=get_user_model().objects.create_superuser(email="email@gmail.com",first_name= "first_name",last_name= "last_name",password=None)
        self.client.force_authenticate(user)

        #first check area code beneath limits
        response = self.client.post(
            '/api/team/', {'category': "a"*100, 'name': "d"*100})
        self.assertEquals(response.status_code, 200)

        #now exceed name limit
        response = self.client.post(
            '/api/team/', {'category': "a"*100, 'name': "d"*101})
        self.assertEquals(response.status_code, 400)

        #now exceed category limit
        response = self.client.post(
            '/api/team/', {'category': "a"*101, 'name': "d"*100})
        self.assertEquals(response.status_code, 400)