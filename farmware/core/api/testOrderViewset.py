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
# 0001_initial,0002_initial,0003_auto_20221018_0824,0004_auto_20221018_1055,0005_auto_20221018_1132
from .urls import *
from django_test_migrations.contrib.unittest_case import MigratorTestCase
from django.test import Client
from rest_framework.test import APITestCase

# Tests the Order Viewset (doesn't include orderitem or orderitemstocklink)
class OrderViewsetTestCases(APITestCase):

    #setup organisation, as well as a customer to create orders
    def setUp(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmone", logo="goat")
        org = Organisation.objects.get(name="Farmone")
        #create customer, required to create orders.
        customer = Customer.objects.create(
            organisation=org, name="Henry", phone_number="9191223445")


    #Test creating an order
    def test_creating(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)
        customer = Customer.objects.get(name="Henry")
        response = self.client.post(
            '/api/order/', {'organisation': org, 'customer_id': customer.pk, 'order_date': "2022-10-25", 'completion_date': "2023-10-25"})
        self.assertEquals(response.status_code, 200)

        #test it was created
        self.assertEquals(str(Order.objects.get(customer_id=customer.id).order_date),"2022-10-25")


    #Test deleting an order
    def test_destroying(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)
        customer = Customer.objects.get(name="Henry")
        response = self.client.post(
            '/api/order/', {'organisation': org, 'customer_id': customer.pk, 'order_date': "2022-10-25", 'completion_date': "2023-10-25"})
        self.assertEquals(response.status_code, 200)

        #get the order id
        order_id = Order.objects.get(customer_id=customer.pk).id

        response2 = self.client.delete(f'/api/order/'+str(order_id)+"/")
        self.assertEquals(response2.status_code, 200)

        # Check it no longer exists
        self.assertRaises(Order.DoesNotExist, Order.objects.get, customer_id=customer.pk)


    #Test partial update an order
    def test_partial_update(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)
        customer = Customer.objects.get(name="Henry")
        response = self.client.post(
            '/api/order/', {'organisation': org, 'customer_id': customer.pk, 'order_date': "2022-10-25", 'completion_date': "2023-10-25"})
        self.assertEquals(response.status_code, 200)

        #get the order id
        order_id = Order.objects.get(customer_id=customer.pk).id

        response2 = self.client.patch(
            f'/api/order/'+str(order_id)+"/", {'order_date': "2022-10-26"})
        self.assertEquals(response2.status_code, 200)

        #check it updated
        self.assertEquals(str(Order.objects.get(customer_id=customer.id).order_date),"2022-10-26")

    #Test order update
    def test_update(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)
        customer = Customer.objects.get(name="Henry")
        response = self.client.post(
            '/api/order/', {'organisation': org, 'customer_id': customer.pk, 'order_date': "2022-10-25", 'completion_date': "2023-10-25"})
        self.assertEquals(response.status_code, 200)

        #get the order id
        order_id = Order.objects.get(customer_id=customer.pk).id
        
        response2 = self.client.put(f'/api/order/'+str(order_id)+"/", {'organisation': org,
                                    'customer_id': customer.pk, 'order_date': "2022-10-27", 'completion_date': "2023-10-15"})
        self.assertEquals(response2.status_code, 200)

        #check it updated
        self.assertEquals(str(Order.objects.get(customer_id=customer.id).order_date),"2022-10-27")

    def test_list(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)
        customer = Customer.objects.get(name="Henry")
        response = self.client.post(
            '/api/order/', {'organisation': org, 'customer_id': customer.pk, 'order_date': "2022-10-25"})
        self.assertEquals(response.status_code, 200)

        response_2 = self.client.post(
            '/api/order/', {'organisation': org, 'customer_id': customer.pk, 'order_date': "2022-10-26"})
        self.assertEquals(response.status_code, 200)

        get_response = self.client.get('/api/order/')
        json_response = get_response.json()

        self.assertEquals(len(json_response),2)

        self.assertEquals(json_response[0]['customer_id'],customer.pk)
        self.assertEquals(json_response[0]['order_date'],"2022-10-25")

        self.assertEquals(json_response[1]['customer_id'],customer.pk)
        self.assertEquals(json_response[1]['order_date'],"2022-10-26")


    # Test that the order endpoints are not accessible to an unauthorised user.
    def test_unauthorised_user(self):
        #setup org
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        customer = Customer.objects.get(name="Henry")

        #first, test creating order
        response = self.client.post(
            '/api/order/', {'organisation': org, 'customer_id': customer.pk, 'order_date': "2022-10-25", 'completion_date': "2023-10-25"})
        self.assertEquals(response.status_code, 401)

        #secondly, test deleting customer
        delete_response = self.client.delete(f'/api/order/0/')
        self.assertEquals(delete_response.status_code, 401)

        #thirdly, test partial updating order
        patch_response = self.client.patch(
            '/api/order/0/', {'order_date': "2022-10-26"})
        self.assertEquals(patch_response.status_code, 401)

        #fourthly, test updating customer
        put_response = self.client.put(f'/api/order/0/', {'organisation': org,
                                    'customer_id': customer.pk, 'order_date': "2022-10-27", 'completion_date': "2023-10-15"})
        self.assertEquals(put_response.status_code, 401)

        #lastly, test listing customer
        get_response = self.client.get('/api/order/')
        self.assertEquals(get_response.status_code,401)