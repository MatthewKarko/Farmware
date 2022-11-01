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

class OrderViewsetTestCases(APITestCase):
    def setUp(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code =org_code,name="Farmone",logo="goat")
        organisatio=Organisation.objects.get(name="Farmone")
        produce=Produce.objects.create(organisation=organisatio,name="eggs")
        producequantitysuffix=ProduceQuantitySuffix.objects.create(produce_id=produce,suffix="lorem ipsum",base_equivalent=5.0)
        producevariety=ProduceVariety.objects.create(produce_id=produce,variety="brown")
        supplier=Supplier.objects.create(organisation=organisatio,name = "john",phone_number = "1234567891")
        areacode=AreaCode.objects.create( organisation=organisatio,area_code="204",description="just another area code")
        stock=Stock.objects.create(organisation=organisatio,produce_id =produce,
    variety_id =producevariety,
    quantity = 6.0,
    quantity_suffix_id =producequantitysuffix,
    supplier_id =supplier,
    date_seeded = "2022-10-25",
    date_planted = "2022-10-26",
    date_picked = "2022-10-27",
    ehd = "2022-10-28" ,
    date_completed ="2022-10-29",
    area_code_id=areacode)
        customer=Customer.objects.create(organisation=organisatio,name = "Henry",phone_number="9191223445" )
        order=Order.objects.create(organisation=organisatio,customer_id= customer,order_date="2022-10-25",completion_date="2023-10-25")
        OrderItem.objects.create(order_id =order,produce_id=produce,produce_variety_id =producevariety,quantity = 10.0,quantity_suffix_id =producequantitysuffix)
    def test_creating(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        customer=Customer.objects.get(name="Henry")
        response=self.client.post('/api/order/',{'organisation':organisatio,'customer_id': customer.pk,'order_date':"2022-10-25",'completion_date':"2023-10-25"})
        self.assertEquals(response.status_code,200)
    def test_destroying(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        customer=Customer.objects.get(name="Henry")
        response=self.client.post('/api/order/',{'organisation':organisatio,'customer_id': customer.pk,'order_date':"2022-10-25",'completion_date':"2023-10-25"})
        self.assertEquals(response.status_code,200)
        response2=self.client.delete(f'/api/order/{user.pk}/')
        self.assertEquals(response2.status_code,200)
    def test_partial_update(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        customer=Customer.objects.get(name="Henry")
        response=self.client.post('/api/order/',{'organisation':organisatio,'customer_id': customer.pk,'order_date':"2022-10-25",'completion_date':"2023-10-25"})
        self.assertEquals(response.status_code,200)
        response2=self.client.patch(f'/api/order/{user.pk}/',{'order_date':"2022-10-26"})
        self.assertEquals(response2.status_code,200)
    def test_update(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        customer=Customer.objects.get(name="Henry")
        response=self.client.post('/api/order/',{'organisation':organisatio,'customer_id': customer.pk,'order_date':"2022-10-25",'completion_date':"2023-10-25"})
        self.assertEquals(response.status_code,200)
        response2=self.client.put(f'/api/order/{user.pk}/',{'organisation':organisatio,'customer_id': customer.pk,'order_date':"2022-10-27",'completion_date':"2023-10-15"})
        self.assertEquals(response2.status_code,200)
    def test_list(self):
        organisatio=Organisation.objects.get(name="Farmone")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", organisatio.code, None,is_staff=True)
        self.client.force_authenticate(user)
        customer=Customer.objects.get(name="Henry")
        response=self.client.post('/api/order/',{'organisation':organisatio,'customer_id': customer.pk,'order_date':"2022-10-25",'completion_date':"2023-10-25"})
        self.assertEquals(response.status_code,200)
        response2=self.client.get('/api/order/')
        res=response2.json()
        self.assertEquals(res[0]['order_date'],"2022-10-25")
        