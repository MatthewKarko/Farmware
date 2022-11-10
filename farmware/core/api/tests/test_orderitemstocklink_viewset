from django.contrib.auth import get_user_model
from ..models import *
from ..models.order import *
from rest_framework.test import APITestCase

# Tests the OrderItemStockLink Viewset
class OrderItemStockLinkViewsetTestCases(APITestCase):
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
        produce_quantity_suffix = ProduceQuantitySuffix.objects.create(
            produce_id=produce, suffix="tonne", base_equivalent=1000.0)
        produce_variety = ProduceVariety.objects.create(
            produce_id=produce, variety="Red Apple")

        #Add produce to order
        OrderItem.objects.create(order_id=order, produce_id=produce, produce_variety_id=produce_variety,
                                 quantity=10.0, quantity_suffix_id=produce_quantity_suffix)
        
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
                                     date_completed="2022-10-29",
                                     area_code_id=areacode)

    # Create OrderItemStockLink
    def test_creating(self):
        organisation = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisation.code, None, is_staff=True)
        self.client.force_authenticate(user)
        stock = Stock.objects.get(quantity=6.0)
        orderItem = OrderItem.objects.get(quantity=10.0)
        producequantitysuffix = ProduceQuantitySuffix.objects.get(
            suffix="tonne")
        response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': orderItem.id, 'stock_id': stock.id, 'quantity': 5.0, 'quantity_suffix_id': producequantitysuffix.id})
        self.assertEquals(response.status_code, 201)

        #check it was created
        self.assertEquals(OrderItemStockLink.objects.get(order_item_id=orderItem.id).quantity,5)

    def test_destroying(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)
        stock = Stock.objects.get(quantity=6.0)
        orderItem = OrderItem.objects.get(quantity=10.0)
        producequantitysuffix = ProduceQuantitySuffix.objects.get(
            suffix="tonne")
        response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': orderItem.id, 'stock_id': stock.id, 'quantity': 5.0, 'quantity_suffix_id': producequantitysuffix.id})
        self.assertEquals(response.status_code, 201)

        #get the id for the stock link
        order_item_stock_link_id = OrderItemStockLink.objects.get(order_item_id=orderItem.id).id

        delete_response = self.client.delete('/api/order_item_stock_link/'+str(order_item_stock_link_id)+"/")
        self.assertEquals(delete_response.status_code,200)

        #check was actually deleted
        self.assertRaises(OrderItemStockLink.DoesNotExist, OrderItemStockLink.objects.get, order_item_id=orderItem.id)

    def test_partial_update(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)
        stock = Stock.objects.get(quantity=6.0)
        orderItem = OrderItem.objects.get(quantity=10.0)
        producequantitysuffix = ProduceQuantitySuffix.objects.get(
            suffix="tonne")
        response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': orderItem.pk, 'stock_id': stock.pk, 'quantity': 5.0, 'quantity_suffix_id': producequantitysuffix.pk})
        self.assertEquals(response.status_code, 201)

        #get the id for the stock link
        order_item_stock_link_id = OrderItemStockLink.objects.get(order_item_id=orderItem.id).id

        response=self.client.patch(f'/api/order_item_stock_link/'+str(order_item_stock_link_id)+"/",{'quantity':4.0})
        self.assertEquals(response.status_code,200)

        #check it changed
        self.assertEquals(OrderItemStockLink.objects.get(order_item_id=orderItem.id).quantity,4)

    def test_update(self):
        org = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", org.code, None, is_staff=True)
        self.client.force_authenticate(user)
        stock = Stock.objects.get(quantity=6.0)
        orderItem = OrderItem.objects.get(quantity=10.0)
        producequantitysuffix = ProduceQuantitySuffix.objects.get(
            suffix="tonne")
        response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': orderItem.pk, 'stock_id': stock.pk, 'quantity': 5.0, 'quantity_suffix_id': producequantitysuffix.pk})
        self.assertEquals(response.status_code, 201)

        #get the id for the stock link
        order_item_stock_link_id = OrderItemStockLink.objects.get(order_item_id=orderItem.id).id

        response=self.client.put(f'/api/order_item_stock_link/'+str(order_item_stock_link_id)+"/",{
                                    'order_item_id': orderItem.pk, 'stock_id': stock.pk, 'quantity': 3.0, 'quantity_suffix_id': producequantitysuffix.pk})
        self.assertEquals(response.status_code,200)

        #check it changed
        self.assertEquals(OrderItemStockLink.objects.get(order_item_id=orderItem.id).quantity,3)

    #Test GET request for order item stock link
    def test_list(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        self.client.force_authenticate(user)

        #add a few stock links
        stock = Stock.objects.get(quantity=6.0)
        orderItem = OrderItem.objects.get(quantity=10.0)
        producequantitysuffix = ProduceQuantitySuffix.objects.get(
            suffix="tonne")
        response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': orderItem.id, 'stock_id': stock.id, 'quantity': 5.0, 'quantity_suffix_id': producequantitysuffix.id})
        self.assertEquals(response.status_code, 201)

        response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': orderItem.id, 'stock_id': stock.id, 'quantity': 7.0, 'quantity_suffix_id': producequantitysuffix.id})
        self.assertEquals(response.status_code, 201)

        #get the ids
        order_item_stock_link_id = OrderItemStockLink.objects.get(order_item_id=orderItem.id, quantity=5).id
        order_item_stock_link_id_2 = OrderItemStockLink.objects.get(order_item_id=orderItem.id, quantity=7).id

        get_response = self.client.get('/api/order_item_stock_link/')
        self.assertEquals(get_response.status_code, 200)
        json_response = get_response.json()

        self.assertEquals(len(json_response),2)

        self.assertEquals(json_response[0]['order_item_id'],orderItem.id)
        self.assertEquals(json_response[0]['quantity'],5.0)

        self.assertEquals(json_response[1]['order_item_id'],orderItem.id)
        self.assertEquals(json_response[1]['quantity'],7.0)

    # Test that the order item stock link endpoints are not accessible to an unauthorised user.
    def test_unauthorised_user(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        stock = Stock.objects.get(quantity=6.0)
        orderItem = OrderItem.objects.get(quantity=10.0)
        producequantitysuffix = ProduceQuantitySuffix.objects.get(
            suffix="tonne")

        # CREATE
        create_response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': orderItem.id, 'stock_id': stock.id, 'quantity': 5.0, 'quantity_suffix_id': producequantitysuffix.id})
        self.assertEquals(create_response.status_code, 401)

        # delete
        delete_response = self.client.delete('/api/order_item_stock_link/0/')
        self.assertEquals(delete_response.status_code,401)

        #PATCH
        patch_response=self.client.patch(f'/api/order_item_stock_link/0/',{'quantity':4.0})
        self.assertEquals(patch_response.status_code,401)

        #PUT
        put_response=self.client.put(f'/api/order_item_stock_link/0/',{
                                    'order_item_id': orderItem.pk, 'stock_id': stock.pk, 'quantity': 3.0, 'quantity_suffix_id': producequantitysuffix.pk})
        self.assertEquals(put_response.status_code,401)

        get_response = self.client.get('/api/order_item_stock_link/')
        self.assertEquals(get_response.status_code, 401)
    
    #Tests field validation in order item stock link endpoint
    def test_field_validation(self):
        organisatio = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisatio.code, None, is_staff=True)
        self.client.force_authenticate(user)
        stock = Stock.objects.get(quantity=6.0)
        orderItem = OrderItem.objects.get(quantity=10.0)
        producequantitysuffix = ProduceQuantitySuffix.objects.get(
            suffix="tonne")

        response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': orderItem.id, 
                                    'stock_id': stock.id, 
                                    'quantity': 5.0, 
                                    'quantity_suffix_id': producequantitysuffix.id})
        self.assertEquals(response.status_code, 201)

        #invalid order item id
        response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': 123, 
                                    'stock_id': stock.id, 
                                    'quantity': 5.0, 
                                    'quantity_suffix_id': producequantitysuffix.id})
        self.assertEquals(response.status_code, 400)

        #invalid stock id
        response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': orderItem.id, 
                                    'stock_id': 123, 
                                    'quantity': 5.0, 
                                    'quantity_suffix_id': producequantitysuffix.id})
        self.assertEquals(response.status_code, 400)

        #invalid quantity suffix id
        response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': orderItem.id, 
                                    'stock_id': stock.id, 
                                    'quantity': 5.0, 
                                    'quantity_suffix_id': 123})
        self.assertEquals(response.status_code, 400)

        #invalid quantity
        response = self.client.post('/api/order_item_stock_link/', {
                                    'order_item_id': orderItem.id, 
                                    'stock_id': stock.id, 
                                    'quantity': "abc5.0", 
                                    'quantity_suffix_id': producequantitysuffix.id})
        self.assertEquals(response.status_code, 400)