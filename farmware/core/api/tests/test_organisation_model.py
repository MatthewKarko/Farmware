from django.test import TestCase
from ..models import *

class OrganisationTestCases(TestCase):
    def setUp(self):
        self.org_code = generate_random_org_code()
        self.name = "Org"
        self.logo = "img"
        self.org = Organisation.objects.create(code = self.org_code, name = self.name, logo = self.logo)
    
    def test_organisation_fields(self):
        self.assertEquals(self.org.name, self.name)
        self.assertEquals(self.org.logo, self.logo)