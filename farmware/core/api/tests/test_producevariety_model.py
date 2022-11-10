from django.test import TestCase
from ..models import *

class ProduceVarietyTestCases(TestCase):
    def setUp(self):
        self.org_code = generate_random_org_code()
        self.org = Organisation.objects.create(code = self.org_code, name = "Org", logo = "img")
        self.p_name = "Eggs"
        self.p = Produce.objects.create(organisation=self.org, name=self.p_name)
        self.pv_name = "Variety"
        self.pv = ProduceVariety.objects.create(variety=self.pv_name, produce_id=self.p)

    def test_ProduceVariety(self):
        self.assertEquals(self.pv.variety, self.pv_name)
        self.assertEquals(self.pv.produce_id, self.p)