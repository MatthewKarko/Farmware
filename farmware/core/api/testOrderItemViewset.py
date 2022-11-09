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
from django.http import JsonResponse

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

    #Test get_available_stock
    def test_get_available_stock(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)

        # create order
        customer = Customer.objects.create(
            organisation=org, name="Henry", phone_number="9191223445")
        order = Order.objects.create(organisation=org, customer_id=customer,
                                     order_date="2022-10-25", completion_date="2023-10-25")

        # # create a produce can use in tests
        produce = Produce.objects.create(organisation=org, name="Banana")
        produce_quantity_suffix = ProduceQuantitySuffix.objects.create(
            produce_id=produce, suffix="tonne", base_equivalent=1000.0)
        produce_variety = ProduceVariety.objects.create(
            produce_id=produce, variety="Yellow Banana")

        # #Add produce to order
        # order_item = OrderItem.objects.create(order_id=order, produce_id=produce, produce_variety_id=produce_variety,
        #                          quantity=1.0, quantity_suffix_id=produce_quantity_suffix)

        #create order item
        post_response = self.client.post("/api/order_item/", {
            'order_id': order.id,
            'produce_id': produce.id,
            'produce_variety_id': produce_variety.id,
            'quantity_suffix_id': produce_quantity_suffix.id,
            'quantity': 1
        })
        self.assertEquals(post_response.status_code, 201)

        #get the order item
        order_item_obj = OrderItem.objects.get(order_id=order.id,quantity=1)
        # self.assertEquals(OrderItem.objects.get(order_id=order.id).quantity,10)

        #create stock to be used in testing
        supplier = Supplier.objects.create(
            organisation=org, name="john", phone_number="1234567891")
        areacode = AreaCode.objects.create(
            organisation=org, area_code="204", description="just another area code")
        stock = Stock.objects.create(organisation=org, produce_id=produce,
                                     variety_id=produce_variety,
                                     quantity=6.0,
                                     quantity_suffix_id=produce_quantity_suffix,
                                     supplier_id=supplier,
                                     date_seeded="2022-10-25",
                                     date_planted="2022-10-26",
                                     date_picked="2022-10-27",
                                     ehd="2022-10-28",
                                     area_code_id=areacode)
        
        #create another stock
        stock = Stock.objects.create(organisation=org, produce_id=produce,
                                     variety_id=produce_variety,
                                     quantity=4.0,
                                     quantity_suffix_id=produce_quantity_suffix,
                                     supplier_id=supplier,
                                     date_seeded="2022-10-25",
                                     date_planted="2022-10-26",
                                     date_picked="2022-10-27",
                                     ehd="2022-10-28",
                                     area_code_id=areacode)

        #test the get
        get_available_stock_response = self.client.get('/api/order_item/'+str(order_item_obj.id)+"/get_available_stock/")
        self.assertEquals(get_available_stock_response.status_code, 200)

        # print(get_available_stock_response.json())

        # #check the contents is right
        json_response = get_available_stock_response.json()['stock']

        # print(json_response)

        self.assertEquals(len(json_response),2)

        self.assertEquals(json_response[0]['produce_name'],"Banana")
        self.assertEquals(json_response[0]['quantity'],6)

        self.assertEquals(json_response[1]['produce_name'],"Banana")
        self.assertEquals(json_response[1]['quantity'],4)

    #Tests GET /api/order_item/{id}/get_assigned_stock/ and POST /api/order_item/{id}/bulk_add_stock/
    def test_bulk_assign_stock_and_get_assigned_stock(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)

        # create order
        customer = Customer.objects.create(
            organisation=org, name="Henry", phone_number="9191223445")
        order = Order.objects.create(organisation=org, customer_id=customer,
                                     order_date="2022-10-25")

        # # create a produce can use in tests
        produce = Produce.objects.create(organisation=org, name="Banana")
        produce_quantity_suffix = ProduceQuantitySuffix.objects.create(
            produce_id=produce, suffix="tonne", base_equivalent=1000.0)
        produce_variety = ProduceVariety.objects.create(
            produce_id=produce, variety="Yellow Banana")

        #create order item
        post_response = self.client.post("/api/order_item/", {
            'order_id': order.id,
            'produce_id': produce.id,
            'produce_variety_id': produce_variety.id,
            'quantity_suffix_id': produce_quantity_suffix.id,
            'quantity': 10
        })
        self.assertEquals(post_response.status_code, 201)

        #get the order item
        order_item_obj = OrderItem.objects.get(order_id=order.id,quantity=10)

        #create stock to be used in testing
        supplier = Supplier.objects.create(
            organisation=org, name="john", phone_number="1234567891")
        areacode = AreaCode.objects.create(
            organisation=org, area_code="204", description="just another area code")
        stock = Stock.objects.create(organisation=org, produce_id=produce,
                                     variety_id=produce_variety,
                                     quantity=6.0,
                                     quantity_suffix_id=produce_quantity_suffix,
                                     supplier_id=supplier,
                                     area_code_id=areacode)
        
        #create another stock
        stock_2 = Stock.objects.create(organisation=org, produce_id=produce,
                                     variety_id=produce_variety,
                                     quantity=4.0,
                                     quantity_suffix_id=produce_quantity_suffix,
                                     supplier_id=supplier,
                                     area_code_id=areacode)

        #bulk assign stock
        # {'items':['stock_id':1, 'quantity':10, 'quantity_suffix_id':0]}

        request_json = {
            'items': [
                {
                    'stock_id': stock.id,
                    'quantity': 1,
                    'quantity_suffix_id': produce_quantity_suffix.id 
                },
                {
                    'stock_id': stock_2.id,
                    'quantity': 2,
                    'quantity_suffix_id': produce_quantity_suffix.id
                }
            ]
        }
        
        post_response = self.client.post("/api/order_item/"+str(order_item_obj.id)+"/bulk_add_stock/", 
            JsonResponse(request_json))

        self.assertEquals(post_response.status_code, 201)

        #check the stock was added
        get_assigned_stock_response = self.client.get('/api/order_item/'+str(order_item_obj.id)+"/get_assigned_stock/")
        self.assertEquals(get_assigned_stock_response.status_code, 200)

        # Check response content
        json_response = get_assigned_stock_response.json()['stock']
        self.assertEquals(len(json_response),2)

        self.assertEquals(json_response[0]['produce_name'],"Banana")
        self.assertEquals(json_response[0]['quantity'],1)
        self.assertEquals(json_response[0]['stock_id'],stock.id)

        self.assertEquals(json_response[1]['produce_name'],"Banana")
        self.assertEquals(json_response[1]['quantity'],2)
        self.assertEquals(json_response[1]['stock_id'],stock_2.id)
