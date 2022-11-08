import json
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

#Test the AreaCode API endpoints using create_user permission levels.
class AreaCodeViewsetTestCases(APITestCase):
    def setUp(self):
        # generating the org_code needed to create the organisation object
        org_code = generate_random_org_code()
        # created organisation using the org_code
        Organisation.objects.create(code=org_code, name="Farmone", logo="goat")

    # Test creation of area code using POST to /api/area_code/ endpoint
    def test_creating(self):
        # getting the newly created object
        organisatio = Organisation.objects.get(name="Farmone")
        # creating the user
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        # forcing the authentication
        self.client.force_authenticate(user)
        # now ,its time to send a post request to create the areacode object , i have just created and sent the data without naming it
        response = self.client.post(
            '/api/area_code/', {'organisation': organisatio.name, 'area_code': 000000, 'description': "all good"})
        # here i am checking the status code for success
        self.assertEquals(response.status_code, 200)

        #check was added correctly
        self.assertEquals(AreaCode.objects.get(area_code=000000).description,"all good")

    # Test deleting an area code using DELETE to /api/area_code/{id}/ endpoint
    def test_destroying(self):
        # First, create an area code.
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/api/area_code/', {'organisation': organisatio.name, 'area_code': 111111, 'description': "all good"})
        self.assertEquals(response.status_code, 200)

        # Get the id of the area code created
        area_code_index = AreaCode.objects.get(area_code=111111).id
        # Delete the area code
        delete_response = self.client.delete('/api/area_code/'+str(area_code_index)+'/')
        self.assertEquals(delete_response.status_code,200)

        #check it was infact deleted
        self.assertRaises(AreaCode.DoesNotExist, AreaCode.objects.get, area_code=111111)

    # Test partially updating area code works using PATCH to /api/area_code/{id}/ endpoint
    def test_partial_update(self):
        # same thing as usual
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/api/area_code/', {'organisation': organisatio.name, 'area_code': 222222, 'description': "test desc"})
        self.assertEquals(response.status_code, 200)
        
        # Get the id of the area code created
        area_code_index = AreaCode.objects.get(area_code=222222).id

        patch_response = self.client.patch('/api/area_code/'+str(area_code_index)+'/', {'description': "new test desc"})
        self.assertEquals(patch_response.status_code, 200)

        #check it did change
        self.assertEquals(AreaCode.objects.get(area_code=222222).description,"new test desc")

    # Test updating area code works using PUT to /api/area_code/{id}/ endpoint
    def test_update(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/api/area_code/', {'area_code': 333333, 'description': "all good"})
        self.assertEquals(response.status_code, 200)

        area_code_index = AreaCode.objects.get(area_code=333333).id

        put_response = self.client.put('/api/area_code/'+str(area_code_index)+'/', { 'area_code': '333333', 'description': "all seems to be good"})
        self.assertEquals(put_response.status_code, 200)

        # Check it updated
        self.assertEquals(AreaCode.objects.get(area_code=333333).description,"all seems to be good")

    # Test listing all of the area codes using GET /api/area_code/ endpoint
    def test_list(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        self.client.force_authenticate(user)
        self.client.post(
            '/api/area_code/', {'organisation': organisatio.name, 'area_code': 000000, 'description': "all good"})
        self.client.post(
            '/api/area_code/', {'organisation': organisatio.name, 'area_code': 111111, 'description': "all good again"})
        # this one is the most easiest of them all , all you have to do is call the path using get and that's it
        get_response = self.client.get('/api/area_code/')
        self.assertEquals(get_response.status_code,200)

        #Convert response to json
        json_response = get_response.json()

        #check the json response is correct
        self.assertEquals(len(json_response),2)

        self.assertEquals(int(json_response[0]['area_code']),000000)
        self.assertEquals(json_response[0]['description'],"all good")

        self.assertEquals(int(json_response[1]['area_code']),111111)
        self.assertEquals(json_response[1]['description'],"all good again")


    # Test that the area code endpoints are not accessible to an unauthorised user.
    def test_unauthorised_user(self):
        #setup org
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        #first, test creating area code
        response = self.client.post(
            '/api/area_code/', {'organisation': organisatio.name, 'area_code': 000000, 'description': "all good"})
        # here i am checking the status code for success
        self.assertEquals(response.status_code, 401)

        #secondly, test deleting area code
        delete_response = self.client.delete('/api/area_code/0/')
        self.assertEquals(delete_response.status_code,401)

        #thirdly, test partial updating area code
        patch_response = self.client.patch('/api/area_code/0/', {'description': "new test desc"})
        self.assertEquals(patch_response.status_code, 401)

        #fourthly, test updating area code
        put_response = self.client.patch('/api/area_code/0/', { 'area_code': '333333', 'description': "all seems to be good"})
        self.assertEquals(put_response.status_code, 401)

        #lastly, test listing area codes
        get_response = self.client.get('/api/area_code/')
        self.assertEquals(get_response.status_code,401)
