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

#for the files ending with the "*viewset.py" i am trying to reach their actions which are in general create,delete,partial_update,update and  trying to get list as well. One thing to keep in mind is that we don't need any user with special privledges for this one but for produce* viewsets we need one. There i used create_superuser instead of just create_user
#another thing is that i am using APITestCase instead of the normal TestCase  as it has its own client which will help in reaching the endpoints and most importantly in forcing the authentication
class AreaCodeViewsetTestCases(APITestCase):
    def setUp(self):
        #setting things up
        #generating the org_code needed to create the organisation object
        org_code=generate_random_org_code()
        #created it using the org_code
        Organisation.objects.create(code =org_code,name="Farmone",logo="goat")
    def test_creating(self):
        #getting the newly created object
        organisatio=Organisation.objects.get(name="Farmone")
        #creating the user
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        #forcing the authentication
        self.client.force_authenticate(user)
        #now ,its time to send a post request to create the areacode object , i have just created and sent the data without naming it
        response=self.client.post('/api/area_code/',{'organisation':organisatio.name,'area_code':000000,'description':"all good"})
        #here i am checking the status code for success
        self.assertEquals(response.status_code,200)
    def test_destroying(self):
        #i am creating the areacode object first for every test and then  i am doing the different stuff needed for that test like here we need to destroy the object we just created.
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        response=self.client.post('/api/area_code/',{'organisation':organisatio.name,'area_code':000000,'description':"all good"})
        self.assertEquals(response.status_code,200)
        # time to destroy it by sending in the lookup which is user.pk
        # do make sure to add a f before the '' of the path in order to replace the text user.pk with actual number
        response2=self.client.delete(f'/api/area_code/{user.pk}/')
        #checking it
        self.assertEquals(response2.status_code,200)
    def test_partial_update(self):
        #same thing as usual
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        response=self.client.post('/api/area_code/',{'organisation':organisatio.name,'area_code':000000,'description':"all good"})
        self.assertEquals(response.status_code,200)
        #now we are updating it with some new stuff , i have just updated the description and that is why it is partial update
        #notice patch instead of post
        response2=self.client.patch(f'/api/area_code/{user.pk}/',{'description':"all not good"})
        self.assertEquals(response2.status_code,200)
    def  test_update(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        response=self.client.post('/api/area_code/',{'organisation':organisatio.name,'area_code':000000,'description':"all good"})
        self.assertEquals(response.status_code,200)
        #here to update it completely instead of using the partial update we need to send in every detail instead of just one like description in the earlier one
        #also notice that to do so we need to use put instead of post
        org_code=generate_random_org_code()
        Organisation.objects.create(code =org_code,name="Farmtwo",logo="sheep")
        organisatio2=Organisation.objects.get(name="Farmtwo")
        #for partial_update , update , delete we need to specify the lookup or the user.pk
        response2=self.client.put(f'/api/area_code/{user.pk}/',{'organisation':organisatio2,'area_code':'000001','description':"all seems to be good"})
        self.assertEquals(response2.status_code,200)
    def test_list(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        response=self.client.post('/api/area_code/',{'organisation':organisatio.name,'area_code':000000,'description':"all good"})
        self.assertEquals(response.status_code,200)
        #this one is the most easiest of them all , all you have to do is call the path using get and that's it
        response2=self.client.get('/api/area_code/')
        #here i am converting it to json
        res=response2.json()
        #here i am trying to access the list for the desctiption and checking whether it has what i gave it or not
        self.assertEquals(res[0]['description'],"all good")
