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

class StockTestCases(TestCase):
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
        self.qty = 123
        self.aqty = 123
        self.date_seeded = "2022-10-01"
        self.date_planted = "2022-10-02"
        self.date_picked = "2022-10-03"
        self.ehd = "2022-12-01"
        self.stock = Stock.objects.create(organisation=self.org, quantity=self.qty, quantity_available=self.aqty, date_seeded=self.date_seeded, date_planted = self.date_planted, date_picked = self.date_picked, ehd = self.ehd, date_completed = None, produce_id = self.p, variety_id = self.pv, quantity_suffix_id = self.pqs, supplier_id = self.s, area_code_id = self.ac)

    # Test whether the fields of the created stock are correct or not
    def test_stock_fields(self):
        self.assertEquals(self.stock.quantity, self.qty)
        self.assertEquals(self.stock.quantity_available, self.aqty)
        self.assertEquals(self.stock.date_seeded, self.date_seeded)
        self.assertEquals(self.stock.date_planted, self.date_planted)
        self.assertEquals(self.stock.date_picked, self.date_picked)
        self.assertEquals(self.stock.ehd, self.ehd)
        self.assertEquals(self.stock.date_completed, None)
        self.assertEquals(self.stock.produce_id, self.p)
        self.assertEquals(self.stock.variety_id, self.pv)
        self.assertEquals(self.stock.quantity_suffix_id, self.pqs)
        self.assertEquals(self.stock.supplier_id, self.s)
        self.assertEquals(self.stock.area_code_id, self.ac)

    # Ensure that null org raises integrity error
    def test_stock_creation_exception(self):
        with self.assertRaises(IntegrityError):
            Stock.objects.create(organisation=None, quantity_available=self.aqty, date_seeded=self.date_seeded, date_planted = self.date_planted, date_picked = self.date_picked, ehd = self.ehd, date_completed = None, produce_id = self.p, variety_id = self.pv, quantity_suffix_id = self.pqs, supplier_id = self.s, area_code_id = self.ac)