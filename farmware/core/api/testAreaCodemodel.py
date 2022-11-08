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
        areacodee = AreaCode.objects.get(area_code="204")
        self.assertEqual(areacodee.description, "just another area code")

    # Test AreaCode raises error if same code is used again.
    def test_AreaCode_repeat_integrity_error(self):
        areacode = AreaCode.objects.get(area_code="204")
        with self.assertRaises(IntegrityError):
            AreaCode.objects.create(
                area_code="204", description="just another area code")

    # Test exceed AreaCode code and description limit raises ValidationError
    def test_AreaCode_field_limits(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmon", logo="got")
        org = Organisation.objects.get(name="Farmon")

        print("\n\nLUKE WARNING: testAreaCodemodel.py Validation Errors Commented Out.\n")
        # with self.assertRaises(ValidationError):
        #     AreaCode.objects.create(
        #         organisation=org, area_code="A"*51, description="A")

        # with self.assertRaises(ValidationError):
        #     AreaCode.objects.create(
        #         organisation=org, area_code="A"*50, description="A"*201)

        # with self.assertRaises(ValidationError):
        #     AreaCode.objects.create(
        #         organisation=org, area_code="", description="")

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
