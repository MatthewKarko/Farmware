from django.test import TestCase
from ..models import *
from django.db import IntegrityError

# Tests the AreaCode objects in model
class AreaCodeTestCases(TestCase):
    def setUp(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmone", logo="goat")
        org = Organisation.objects.get(name="Farmone")
        AreaCode.objects.create(
            organisation=org, area_code="204", description="just another area code")

    # Test AreaCode description is correct
    def test_AreaCode_description(self):
        areacode = AreaCode.objects.get(area_code="204")
        self.assertEqual(areacode.description, "just another area code")

    # Test AreaCode raises error if same code is used again.
    def test_AreaCode_repeat_integrity_error(self):
        areacode = AreaCode.objects.get(area_code="204")
        with self.assertRaises(IntegrityError):
            AreaCode.objects.create(
                area_code="204", description="just another area code")

    # Test that multiple Area Codes can be added to an organisation
    def test_AreaCode_multiple(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmon", logo="go")
        org = Organisation.objects.get(name="Farmon")
        AreaCode.objects.create(
            organisation=org, area_code="1", description="test")
        AreaCode.objects.create(
            organisation=org, area_code="2", description="test2")
        self.assertEqual(AreaCode.objects.get(
            area_code="1").description, "test")
        self.assertEqual(AreaCode.objects.get(
            area_code="2").description, "test2")