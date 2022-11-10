# TODO

from django.db import IntegrityError, transaction
from django.test import Client, TestCase

from rest_framework import serializers, exceptions
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient

from ..models import User
from ..serialisers import UserSerialiser
from ...api.models.organisation import Organisation


class UserViewSetTestCases(APITestCase):
    def setUp(self):
        org_code = '000000'

        self.organisation = Organisation.objects.create(
            code=org_code, name="Test Farm", logo="<logo>")

        # User details
        self.first_name = 'Johnny'
        self.last_name = 'Appleseed'
        self.email = 'johnnyappleseed@example.com'
        self.password = "password"

        self.user: User = User.objects.create_user(
            self.email, 
            self.first_name, 
            self.last_name, 
            self.organisation.code, 
            self.password)

    def test_testRegisteringUser(self):
        org= Organisation.objects.get(name="nameoforg")
        response=self.client.post('/api/user/ /register/user/',{'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','org_code':org.code})
        #print(response.content)
        self.assertEquals(response.status_code,201)

    def test_RegisteringUserError(self):
        org= Organisation.objects.get(name="nameoforg")
        response=self.client.post('/api/user/ /register/user/',{'first_name':'firstn','last_name':'lastn','password':'passwd','organisation':org})
        self.assertEquals(response.status_code,400)

    def test_RegisteringAdmin(self):
        user = User.objects.first()
        self.client.force_authenticate(user)
        org= Organisation.objects.get(name="nameoforg")
        response=self.client.post('/api/user/ /register/admin/',{'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','org_name':org.pk})
        self.assertEquals(response.status_code,201)

    def  test_RegisteringAdminError(self):
        serializer_data={}
        response=self.client.post('/api/user/ /register/admin/',serializer_data)
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_estingSettingPasswordsError(self):
        user = User.objects.first()
        self.client.force_authenticate(user)
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','organisation':org}
        response=self.client.post('/api/user/ /set_password/',serializer_data)
        self.assertEquals(response.status_code,405)

    def test_testingSettingPasswords(self):
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','org_code':org.code}
        response=self.client.post('/api/user/ /register/user/',serializer_data)
        self.assertEquals(response.status_code,201)
        user = User.objects.first()
        self.client.force_authenticate(user)
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','old_password':'passwd','new_password':'pass','org_code':org.code}
        respons=self.client.get('/api/user/ /set_password/',serializer_data,args={'pk':user.pk})
        print(respons.content)
        self.assertEquals(respons.status_code,200)

    def test_testingDestroy(self):
        org= Organisation.objects.get(name="nameoforg")
        #name =reverse('user-register-admin')
        #raise ValueError(name)
        response=self.client.post('/api/user/ /register/user/',{'email' : 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','org_name':org.name})
        self.assertEquals(response.status_code,201)
        response2=self.client.delete('/api/user/ /',serializer_data)
        #user=response2[]
        #urlwithid=' /'+user.pk
        #response=c.delete(urlwithid,serializer_data)
        #self.assertEquals(response.status_code,status.HTTP_200_OK)

    def test_testingList(self):
        c = Client()
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','organisation':org}
        response=c.post('/api/user/ /register/user/',serializer_data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        response2=c.get('/api/user/ /',serializer_data)
        self.assertNotEquals(response2,Null)

    def test_testingList(self):
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','org_name':org.name,'role':000}
        respons=self.client.post('/api/user/ /register/admin/',serializer_data)
        self.assertEquals(respons.status_code,status.HTTP_201_CREATED)
        user = User.objects.first()
        self.client.force_authenticate(user)
        response = self.client.get('/api/user/ /')
        self.assertEquals(response.status_code,200)

    def test_testingMyteams(self):
        user = User.objects.first()
        self.client.force_authenticate(user)

        org= Organisation.objects.get(name="nameoforg")
        team=Team.objects.create(category="sports",name="fifa team 12",organisation=org)
        response=self.client.post('/api/user/ /register/user/',{'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','org_code':org.code})
        self.assertEquals(response.status_code,201)
        respones=self.client.get('/api/user/ /teams/',{'user':user})
        self.assertEquals(respones.status_code,200)

    def test_testingUserteams(self):
        user = User.objects.first()
        self.client.force_authenticate(user)
        org=Organisation.objects.get(name="nameoforg")
        team=Team.objects.create(category="sports",name="fifa team 12",organisation=org)
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','org_name':org.name,'team':team}
        response=self.client.post('/api/user/ /register/admin/',serializer_data)
        self.assertEquals(response.status_code,201)
        respons=self.client.get('/api/user/ /teams/',{'user':user})
        #print(respons.content)
        self.assertEquals(respons.status_code,200)
        
    def testingPartialUpdate(self):
        user = User.objects.first()
        self.client.force_authenticate(user)
        org= Organisation.objects.get(name="nameoforg")
        response=self.client.post('/api/user/ /register/user/',{'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','org_code':org.code})
        #print(response.content)
        self.assertEquals(response.status_code,201)
        respons=self.client.patch(f'/api/user/ /{user.pk}/partial_update/',{'first_name':'firstn'})
        #print(respons.content)
        self.assertEquals(respons.status_code,2003)