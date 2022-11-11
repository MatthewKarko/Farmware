from django.test import TestCase
from ..models import *

class SupplierTestCases(TestCase):
    def setUp(self):
        self.org_code = generate_random_org_code()
        self.org = Organisation.objects.create(code = self.org_code, name = "Org", logo="img")
        self.s_name = "Supplier"
        self.s_pn = "012456789"
        self.s = Supplier.objects.create(organisation=self.org, name = self.s_name, phone_number = self.s_pn)
        self.s2 = Supplier.objects.create(organisation=self.org, name = self.s_name+"2", phone_number = self.s_pn+"2")

    # Checking whether the supplier objects have been created correctly
    def test_SupplierFields(self):
        self.assertEquals(self.s.name, self.s_name)
        self.assertEquals(self.s.phone_number, self.s_pn)
        self.assertEquals(self.s2.name, self.s_name+"2")
        self.assertEquals(self.s2.phone_number, self.s_pn+"2")

    def test_SupplierCreationException(self):
        with self.assertRaises(ValueError):
            Supplier.objects.create(organisation=0, phone_number=self.s_pn)