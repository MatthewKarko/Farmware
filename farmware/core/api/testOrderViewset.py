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

        response2 = self.client.delete('/api/order/'+str(order_id)+"/")
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
            '/api/order/'+str(order_id)+"/", {'order_date': "2022-10-26"})
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
        
        response2 = self.client.put('/api/order/'+str(order_id)+"/", {'organisation': org,
                                    'customer_id': customer.pk, 'order_date': "2022-10-27", 'completion_date': "2023-10-15"})
        self.assertEquals(response2.status_code, 200)

        #check it updated
        self.assertEquals(str(Order.objects.get(customer_id=customer.id).order_date),"2022-10-27")

    #Test get all orders
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
        delete_response = self.client.delete('/api/order/0/')
        self.assertEquals(delete_response.status_code, 401)

        #thirdly, test partial updating order
        patch_response = self.client.patch(
            '/api/order/0/', {'order_date': "2022-10-26"})
        self.assertEquals(patch_response.status_code, 401)

        #fourthly, test updating customer
        put_response = self.client.put('/api/order/0/', {'organisation': org,
                                    'customer_id': customer.pk, 'order_date': "2022-10-27", 'completion_date': "2023-10-15"})
        self.assertEquals(put_response.status_code, 401)

        #lastly, test listing customer
        get_response = self.client.get('/api/order/')
        self.assertEquals(get_response.status_code,401)
    
    #Test GET /api/order/{id}/get_order_items/
    def test_get_order_items(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)
        customer = Customer.objects.get(name="Henry")

        # create order
        customer = Customer.objects.create(
            organisation=org, name="Henry", phone_number="9191223445")
        order = Order.objects.create(organisation=org, customer_id=customer,
                                     order_date="2022-10-25", completion_date="2023-10-25")

        # create a produce can use in tests
        produce = Produce.objects.create(organisation=org, name="Apple")
        produce_quantity_suffix = ProduceQuantitySuffix.objects.create(
            produce_id=produce, suffix="tonne", base_equivalent=1000.0)
        produce_variety = ProduceVariety.objects.create(
            produce_id=produce, variety="Red Apple")

        #create order first order item
        post_response = self.client.post("/api/order_item/", {
            'order_id': order.id,
            'produce_id': produce.id,
            'produce_variety_id': produce_variety.id,
            'quantity_suffix_id': produce_quantity_suffix.id,
            'quantity': 10
        })
        self.assertEquals(post_response.status_code, 201)

        #create order second order item
        post_response = self.client.post("/api/order_item/", {
            'order_id': order.id,
            'produce_id': produce.id,
            'produce_variety_id': produce_variety.id,
            'quantity_suffix_id': produce_quantity_suffix.id,
            'quantity': 6
        })
        self.assertEquals(post_response.status_code, 201)

        #test the get
        get_order_items_response = self.client.get('/api/order/'+str(order.id)+"/get_order_items/")
        self.assertEquals(get_order_items_response.status_code, 200)

        #check the contents is right
        json_response = get_order_items_response.json()['order_items']

        self.assertEquals(len(json_response),2)

        self.assertEquals(json_response[0]['order_id'],order.id)
        self.assertEquals(json_response[0]['quantity'],10)

        self.assertEquals(json_response[1]['order_id'],order.id)
        self.assertEquals(json_response[1]['quantity'],6)
    
    #Tests field validation in order endpoint
    def test_field_validation(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)
        customer = Customer.objects.get(name="Henry")

        response = self.client.post(
            '/api/order/', {'customer_id': customer.pk, 'order_date': "2022-10-25", 'completion_date': "2023-10-25"})
        self.assertEquals(response.status_code, 200)

        #invalid customer
        response = self.client.post(
            '/api/order/', {'customer_id': 123, 'order_date': "2022-10-25", 'completion_date': "2023-10-25"})
        self.assertEquals(response.status_code, 400)

        #no order date
        response = self.client.post(
            '/api/order/', {'customer_id': customer.pk})
        self.assertEquals(response.status_code, 400)

        #invoice number valid
        response = self.client.post(
            '/api/order/', {'customer_id': customer.pk, 'order_date': "2022-10-25", 'invoice_number': 123})
        self.assertEquals(response.status_code, 200)

        #invoice number valid string
        response = self.client.post(
            '/api/order/', {'customer_id': customer.pk, 'order_date': "2022-10-25", 'invoice_number': "123"})
        self.assertEquals(response.status_code, 200)

        #invoice number too long
        response = self.client.post(
            '/api/order/', {'customer_id': customer.pk, 'order_date': "2022-10-25", 'invoice_number': "a"*21})
        self.assertEquals(response.status_code, 400)