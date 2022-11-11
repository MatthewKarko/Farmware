from django.test import TestCase
from ..models import *

# Tests the Customer objects in model
class CustomerTestCases(TestCase):
    def setUp(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmone", logo="goat")
        organisation = Organisation.objects.get(name="Farmone")
        Customer.objects.create(organisation=organisation,
                                name="Henry", phone_number="9191223445")

    #Test that the created customer fields are set correctly.
    def test_Customer_fields(self):
        customer = Customer.objects.get(name="Henry")
        self.assertEqual(customer.phone_number, "9191223445")

    #Test that multiple customers can be added to the organisation
    def test_Customer_multiple(self):
        org = Organisation.objects.get(name="Farmone")
        Customer.objects.create(organisation=org, name="Billy Brown", phone_number="9119119123")
        Customer.objects.create(organisation=org, name="Sam Brown", phone_number="1233213211")
        Customer.objects.create(organisation=org, name="Xyz", phone_number="1231231231")

        customer = Customer.objects.get(name="Billy Brown")
        self.assertEqual(customer.phone_number, "9119119123")
        customer = Customer.objects.get(name="Sam Brown")
        self.assertEqual(customer.phone_number, "1233213211")
        customer = Customer.objects.get(name="Xyz")
        self.assertEqual(customer.phone_number, "1231231231")
