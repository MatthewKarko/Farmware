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

# Tests the OrderItem Viewset (doesn't include OrderItemStockLink)
class OrderItemViewsetTestCases(APITestCase):
    def setUp(self):
        # Create organisation
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmone", logo="goat")
        org = Organisation.objects.get(name="Farmone")

        # create order
        customer = Customer.objects.create(
            organisation=org, name="Henry", phone_number="9191223445")
        order = Order.objects.create(organisation=org, customer_id=customer,
                                     order_date="2022-10-25", completion_date="2023-10-25")

        # create a produce can use in tests
        produce = Produce.objects.create(organisation=org, name="Apple")
        producequantitysuffix = ProduceQuantitySuffix.objects.create(
            produce_id=produce, suffix="tonne", base_equivalent=1000.0)
        producevariety = ProduceVariety.objects.create(
            produce_id=produce, variety="Red Apple")

    def test_creating(self):
        org = Organisation.objects.get(name="Farmone")
        customer = Customer.objects.get(name="Henry")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)

        # use created order and produce
        order = Order.objects.get(order_date="2022-10-25")
        produce = Produce.objects.get(name="Apple")
        produce_variety = ProduceVariety.objects.get(variety="Red Apple")
        produce_quantity_suffix = ProduceQuantitySuffix.objects.get(suffix="tonne")

        #create order item
        post_response = self.client.post("/api/order_item/", {
            'order_id': order.id,
            'produce_id': produce.id,
            'produce_variety_id': produce_variety.id,
            'quantity_suffix_id': produce_quantity_suffix.id,
            'quantity': 10
        })
        self.assertEquals(post_response.status_code, 201)

        #check it was created
        self.assertEquals(OrderItem.objects.get(order_id=order.id).quantity,10)


    def test_destroying(self):
        org = Organisation.objects.get(name="Farmone")
        customer = Customer.objects.get(name="Henry")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)

        # use created order and produce
        order = Order.objects.get(order_date="2022-10-25")
        produce = Produce.objects.get(name="Apple")
        produce_variety = ProduceVariety.objects.get(variety="Red Apple")
        produce_quantity_suffix = ProduceQuantitySuffix.objects.get(suffix="tonne")

        #first, create order item
        response = self.client.post("/api/order_item/", {
            'order_id': order.id,
            'produce_id': produce.id,
            'produce_variety_id': produce_variety.id,
            'quantity_suffix_id': produce_quantity_suffix.id,
            'quantity': 10
        })
        self.assertEquals(response.status_code, 201)

        #get the id of order item
        order_item_id = OrderItem.objects.get(order_id=order.id).id

        #now delete the orderitem
        delete_response = self.client.delete('/api/order_item/'+str(order_item_id)+"/")
        self.assertEquals(delete_response.status_code, 200)

        #check it was deleted
        self.assertRaises(OrderItem.DoesNotExist, OrderItem.objects.get, order_id=order.id)

    def test_partial_update(self):
        org = Organisation.objects.get(name="Farmone")
        customer = Customer.objects.get(name="Henry")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)

        # use created order and produce
        order = Order.objects.get(order_date="2022-10-25")
        produce = Produce.objects.get(name="Apple")
        produce_variety = ProduceVariety.objects.get(variety="Red Apple")
        produce_quantity_suffix = ProduceQuantitySuffix.objects.get(suffix="tonne")

        #first, create order item
        response = self.client.post("/api/order_item/", {
            'order_id': order.id,
            'produce_id': produce.id,
            'produce_variety_id': produce_variety.id,
            'quantity_suffix_id': produce_quantity_suffix.id,
            'quantity': 10
        })
        self.assertEquals(response.status_code, 201)

        #get the id of order item
        order_item_id = OrderItem.objects.get(order_id=order.id).id

        #now patch it
        patch_response = self.client.patch(
            '/api/order_item/'+str(order_item_id)+"/", {'quantity': 20.0})
        self.assertEquals(patch_response.status_code, 200)

        #check it changed
        self.assertEquals(OrderItem.objects.get(order_id=order.id).quantity,20)

    def test_update(self):
        org = Organisation.objects.get(name="Farmone")
        customer = Customer.objects.get(name="Henry")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)

        # use created order and produce
        order = Order.objects.get(order_date="2022-10-25")
        produce = Produce.objects.get(name="Apple")
        produce_variety = ProduceVariety.objects.get(variety="Red Apple")
        produce_quantity_suffix = ProduceQuantitySuffix.objects.get(suffix="tonne")

        #first, create order item
        response = self.client.post("/api/order_item/", {
            'order_id': order.id,
            'produce_id': produce.id,
            'produce_variety_id': produce_variety.id,
            'quantity_suffix_id': produce_quantity_suffix.id,
            'quantity': 10
        })
        self.assertEquals(response.status_code, 201)

        #get the id of order item
        order_item_id = OrderItem.objects.get(order_id=order.id).id

        #now patch it
        put_response = self.client.put(
            '/api/order_item/'+str(order_item_id)+"/", {
                'order_id': order.id,
                'produce_id': produce.id,
                'produce_variety_id': produce_variety.id,
                'quantity_suffix_id': produce_quantity_suffix.id,
                'quantity': 12
                })
        self.assertEquals(put_response.status_code, 200)

        #check it changed
        self.assertEquals(OrderItem.objects.get(order_id=order.id).quantity,12)

    def test_list(self):
        org = Organisation.objects.get(name="Farmone")
        customer = Customer.objects.get(name="Henry")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)

        # use created order and produce
        order = Order.objects.get(order_date="2022-10-25")
        produce = Produce.objects.get(name="Apple")
        produce_variety = ProduceVariety.objects.get(variety="Red Apple")
        produce_quantity_suffix = ProduceQuantitySuffix.objects.get(suffix="tonne")

        #first, create order item
        response = self.client.post("/api/order_item/", {
            'order_id': order.id,
            'produce_id': produce.id,
            'produce_variety_id': produce_variety.id,
            'quantity_suffix_id': produce_quantity_suffix.id,
            'quantity': 10
        })
        self.assertEquals(response.status_code, 201)

        #create another order item
        response_2 = self.client.post("/api/order_item/", {
            'order_id': order.id,
            'produce_id': produce.id,
            'produce_variety_id': produce_variety.id,
            'quantity_suffix_id': produce_quantity_suffix.id,
            'quantity': 22
        })
        self.assertEquals(response_2.status_code, 201)

        #now do the get request
        get_response = self.client.get('/api/order_item/')
        self.assertEquals(get_response.status_code, 200)
        json_response = get_response.json()

        self.assertEquals(len(json_response),2)

        self.assertEquals(json_response[0]['order_id'],order.id)
        self.assertEquals(json_response[0]['quantity'],10)

        self.assertEquals(json_response[1]['order_id'],order.id)
        self.assertEquals(json_response[1]['quantity'],22)

    # Test that the order item endpoints are not accessible to an unauthorised user.
    def test_unauthorised_user(self):
        org = Organisation.objects.get(name="Farmone")
        customer = Customer.objects.get(name="Henry")
        order = Order.objects.get(order_date="2022-10-25")
        produce = Produce.objects.get(name="Apple")
        produce_variety = ProduceVariety.objects.get(variety="Red Apple")
        produce_quantity_suffix = ProduceQuantitySuffix.objects.get(suffix="tonne")

        #create order item
        post_response = self.client.post("/api/order_item/", {
            'order_id': order.id,
            'produce_id': produce.id,
            'produce_variety_id': produce_variety.id,
            'quantity_suffix_id': produce_quantity_suffix.id,
            'quantity': 10
        })
        self.assertEquals(post_response.status_code, 401)

        #now delete the orderitem
        delete_response = self.client.delete('/api/order_item/0/')
        self.assertEquals(delete_response.status_code, 401)

        patch_response = self.client.patch(
            '/api/order_item/0/', {'quantity': 20.0})
        self.assertEquals(patch_response.status_code, 401)

        put_response = self.client.put(
            '/api/order_item/0/', {
                'order_id': order.id,
                'produce_id': produce.id,
                'produce_variety_id': produce_variety.id,
                'quantity_suffix_id': produce_quantity_suffix.id,
                'quantity': 12
                })
        self.assertEquals(put_response.status_code, 401)

        get_response = self.client.get('/api/order_item/')
        self.assertEquals(get_response.status_code, 401)