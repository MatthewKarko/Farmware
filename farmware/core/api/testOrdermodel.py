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

# Tests the entire Order model, including Order, OrderItem and OrderItemStockLink
class OrderModelTestCases(TestCase):

    #setup creates the org
    def setUp(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmone", logo="goat")
        organisatio = Organisation.objects.get(name="Farmone")

    #test create order
    def test_create_order(self):
        org = Organisation.objects.get(name="Farmone")

        #create customer and order
        customer = Customer.objects.create(
            organisation=org, name="Henry", phone_number="9191223445")
        order = Order.objects.create(organisation=org, customer_id=customer,
                                     order_date="2022-10-25", completion_date="2023-10-25")
        
        #test the order was created
        self.assertEquals(str(Order.objects.get(order_date="2022-10-25", customer_id=customer.id).completion_date),"2023-10-25")


    #Test create multiple orders
    def test_create_order_multiple(self):
        org = Organisation.objects.get(name="Farmone")

        customer = Customer.objects.create(
            organisation=org, name="Henry", phone_number="9191223445")
        order = Order.objects.create(organisation=org, customer_id=customer,
                                     order_date="2022-10-25", completion_date="2023-10-25")
        
        #test the order was created
        self.assertEquals(str(Order.objects.get(order_date="2022-10-25", customer_id=customer.id).completion_date),"2023-10-25")

        customer_2 = Customer.objects.create(
            organisation=org, name="Bill", phone_number="12312332")
        order = Order.objects.create(organisation=org, customer_id=customer_2,
                                     order_date="2022-10-24", completion_date="2023-10-24")
        
        #test the order was created
        self.assertEquals(str(Order.objects.get(order_date="2022-10-24", customer_id=customer_2.id).completion_date),"2023-10-24")


    #Test create order items
    def test_create_order_item(self):
        org = Organisation.objects.get(name="Farmone")

        #first, create the order
        customer = Customer.objects.create(
            organisation=org, name="Henry", phone_number="9191223445")
        order = Order.objects.create(organisation=org, customer_id=customer,
                                     order_date="2022-10-25", completion_date="2023-10-25")

        #create produce
        produce = Produce.objects.create(organisation=org, name="eggs")
        produce_quantity_suffix = ProduceQuantitySuffix.objects.create(
            produce_id=produce, suffix="kg", base_equivalent=1.0)
        produce_variety = ProduceVariety.objects.create(
            produce_id=produce, variety="brown")

        #add produce to order
        OrderItem.objects.create(order_id = order,produce_id=produce,quantity_suffix_id=produce_quantity_suffix,
            produce_variety_id=produce_variety,quantity=10)
        
        #test it was added
        self.assertEquals(OrderItem.objects.get(order_id=order,produce_id=produce).quantity,10)

        #add more produce
        produce_2 = Produce.objects.create(organisation=org, name="apple")
        produce_quantity_suffix_2 = ProduceQuantitySuffix.objects.create(
            produce_id=produce_2, suffix="tonne", base_equivalent=1000.0)
        produce_variety_2 = ProduceVariety.objects.create(
            produce_id=produce_2, variety="red apple")
        
        OrderItem.objects.create(order_id = order,produce_id=produce_2,quantity_suffix_id=produce_quantity_suffix_2,
            produce_variety_id=produce_variety_2,quantity=1111)
        
        self.assertEquals(OrderItem.objects.get(order_id=order,produce_id=produce_2).quantity,1111)


    def test_create_order_item_stock_link(self):
        org = Organisation.objects.get(name="Farmone")

        #first, create the order
        customer = Customer.objects.create(
            organisation=org, name="Henry", phone_number="9191223445")
        order = Order.objects.create(organisation=org, customer_id=customer,
                                     order_date="2022-10-25", completion_date="2023-10-25")

        #create produce
        produce = Produce.objects.create(organisation=org, name="eggs")
        produce_quantity_suffix = ProduceQuantitySuffix.objects.create(
            produce_id=produce, suffix="kg", base_equivalent=1.0)
        produce_variety = ProduceVariety.objects.create(
            produce_id=produce, variety="brown")

        #create the stock
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
                                     date_completed="2022-10-29",
                                     area_code_id=areacode)
        
        #add produce to order
        order_item = OrderItem.objects.create(order_id = order,produce_id=produce,quantity_suffix_id=produce_quantity_suffix,
            produce_variety_id=produce_variety,quantity=10)

        #assign stock to order item
        OrderItemStockLink.objects.create(order_item_id=order_item,stock_id=stock,quantity=9,quantity_suffix_id=produce_quantity_suffix)

        #check it was added
        self.assertEquals(OrderItemStockLink.objects.get(order_item_id=order_item,stock_id=stock).quantity,9)
