from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ..models import *

class StockViewsetTestCases(APITestCase):
    # Create a Stock item
    def setUp(self):
        self.org_code = generate_random_org_code()
        self.org = Organisation.objects.create(code = self.org_code, name = "Org", logo="img")
        self.p_name = "Eggs"
        self.p = Produce.objects.create(organisation=self.org, name=self.p_name)
        self.pv_name = "Variety"
        self.pv = ProduceVariety.objects.create(variety=self.pv_name, produce_id=self.p)
        self.pqs_suffix = "kg"
        self.pqs_base = 1000
        self.pqs = ProduceQuantitySuffix.objects.create(suffix=self.pqs_suffix, base_equivalent = self.pqs_base, produce_id = self.p)
        self.s_name = "Supplier"
        self.s_pn = "012456789"
        self.s = Supplier.objects.create(organisation=self.org, name = self.s_name, phone_number = self.s_pn)
        self.ac_name = "Area Code"
        self.ac_desc = "It's an area code"
        self.ac = AreaCode.objects.create(organisation=self.org, area_code = self.ac_name, description = self.ac_desc)
        self.qty = 123.0
        self.aqty = 123.0
        self.date_seeded = "2022-10-01"
        self.date_planted = "2022-10-02"
        self.date_picked = "2022-10-03"
        self.ehd = "2022-12-01"
        self.stock = Stock.objects.create(organisation=self.org, quantity=self.qty, quantity_available=self.aqty, date_seeded=self.date_seeded, date_planted = self.date_planted, date_picked = self.date_picked, ehd = self.ehd, date_completed = None, produce_id = self.p, variety_id = self.pv, quantity_suffix_id = self.pqs, supplier_id = self.s, area_code_id = self.ac)
        self.template_list = [{"id":1, "quantity":self.qty, "quantity_available":self.aqty, "date_seeded":self.date_seeded, "date_planted":self.date_planted, "date_picked":self.date_picked, "ehd":self.ehd, "date_completed": None, "organisation":self.org_code, "produce_id": 1, "variety_id": 1, "quantity_suffix_id": 1, "supplier_id": 1, "area_code_id": 1, "produce_name": self.p_name, "variety_name": self.pv_name, "quantity_suffix_name": self.pqs_suffix, "base_equivalent": self.pqs_base, "area_code_name": self.ac_name, "area_code_description": self.ac_desc, "supplier_name": self.s_name, "supplier_phone_number": self.s_pn}]
        self.template = {"id":1, "quantity":self.qty, "quantity_available":self.aqty, "date_seeded":self.date_seeded, "date_planted":self.date_planted, "date_picked":self.date_picked, "ehd":self.ehd, "date_completed": None, "organisation":self.org_code, "produce_id": 1, "variety_id": 1, "quantity_suffix_id": 1, "supplier_id": 1, "area_code_id": 1}
        self.user = get_user_model().objects.create_user("test", "test", "test", self.org_code, None, is_staff=True)
        self.client.force_authenticate(self.user)

    # Test output of GET list
    def test_list(self):
        self.assertJSONEqual(str(self.client.get('/api/stock/').content, encoding='utf-8'), self.template_list)
    
    # Test output of GET read
    def test_read(self):
        self.assertJSONEqual(str(self.client.get('/api/stock/1/').content, encoding='utf-8'), self.template)

    # Test PATCH functionality
    def test_partial_update(self):
        output = self.template
        output["quantity"] = 100.12
        self.assertEquals(self.client.patch('/api/stock/1/', {"quantity":100.12}).status_code, 200)
        self.assertJSONEqual(str(self.client.get('/api/stock/1/').content, encoding='utf-8'), output)
        output["quantity_available"] = 99.99
        self.assertEquals(self.client.patch('/api/stock/1/', {"quantity_available":99.99}).status_code, 200)
        self.assertJSONEqual(str(self.client.get('/api/stock/1/').content, encoding='utf-8'), output)
        output["date_seeded"] = "2022-09-15"
        self.assertEquals(self.client.patch('/api/stock/1/', {"date_seeded":"2022-09-15"}).status_code, 200)
        self.assertJSONEqual(str(self.client.get('/api/stock/1/').content, encoding='utf-8'), output)
        output["date_planted"] = "2022-09-16"
        self.assertEquals(self.client.patch('/api/stock/1/', {"date_planted":"2022-09-16"}).status_code, 200)
        self.assertJSONEqual(str(self.client.get('/api/stock/1/').content, encoding='utf-8'), output)
        output["date_picked"] = "2022-09-17"
        self.assertEquals(self.client.patch('/api/stock/1/', {"date_picked":"2022-09-17"}).status_code, 200)
        self.assertJSONEqual(str(self.client.get('/api/stock/1/').content, encoding='utf-8'), output)
        output["ehd"] = "2022-09-18"
        self.assertEquals(self.client.patch('/api/stock/1/', {"ehd":"2022-09-18"}).status_code, 200)
        self.assertJSONEqual(str(self.client.get('/api/stock/1/').content, encoding='utf-8'), output)
        output["date_completed"] = "2022-12-19"
        self.assertEquals(self.client.patch('/api/stock/1/', {"date_completed":"2022-12-19"}).status_code, 200)
        self.assertJSONEqual(str(self.client.get('/api/stock/1/').content, encoding='utf-8'), output)

    # Test PUT functionality
    def test_update(self):
        output = self.template
        output["quantity"] = 100.12
        output["quantity_available"] = 99.99
        output["date_seeded"] = "2022-09-15"
        output["date_planted"] = "2022-09-16"
        output["date_picked"] = "2022-09-17"
        output["ehd"] = "2022-09-18"
        output["date_completed"] = "2022-12-19"
        self.assertEquals(self.client.put('/api/stock/1/', output).status_code, 200)
        self.assertJSONEqual(str(self.client.get('/api/stock/1/').content, encoding='utf-8'), output)
    
    # Test DELETE functionality
    def test_delete(self):
        self.assertEquals(len(Stock.objects.all()), 1)
        self.assertEquals(self.client.delete('/api/stock/1/').status_code, 200)
        self.assertEquals(len(Stock.objects.all()), 0)

    # Test toggle date completed API endpoint
    def test_toggle_date_completed(self):
        self.assertEquals(self.client.get('/api/stock/1/toggle_date_completed/').status_code, 200)
        self.assertIsNotNone(self.client.get('/api/stock/1/').json()["date_completed"])
        self.assertEquals(self.client.get('/api/stock/1/toggle_date_completed/').status_code, 200)
        self.assertIsNone(self.client.get('/api/stock/1/').json()["date_completed"])
        