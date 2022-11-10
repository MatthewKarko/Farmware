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
from .urls import * #0001_initial,0002_initial,0003_auto_20221018_0824,0004_auto_20221018_1055,0005_auto_20221018_1132
from django_test_migrations.contrib.unittest_case import MigratorTestCase
from django.test import Client
from rest_framework.test import APITestCase

class SupplierViewsetTestCases(APITestCase):
    # Create an initial supplier object
    def setUp(self):
        self.org_code = generate_random_org_code()
        self.org = Organisation.objects.create(code = self.org_code, name = "Org", logo="img")
        self.s_name = "Supplier"
        self.s_pn = "012456789"
        self.s = Supplier.objects.create(organisation=self.org, name = self.s_name, phone_number = self.s_pn)
        self.user = get_user_model().objects.create_user("test", "test", "test", self.org_code, None, is_staff=True)
        self.client.force_authenticate(self.user)
        self.template = {"id":1, "name":self.s_name, "phone_number":self.s_pn, "organisation":self.org_code}

    # Test GET list with one and more than one object
    def test_list(self):
        output = self.template
        self.assertJSONEqual(str(self.client.get('/api/supplier/').content, encoding='utf-8'), [output])
        self.assertEquals(self.client.post('/api/supplier/', {'organisation': self.org, 'name': self.s_name+"2", 'phone_number': self.s_pn+"2"}).status_code, 200)
        output2 = {"id":2, "name":self.s_name+"2", "phone_number":self.s_pn+"2", "organisation":self.org_code}
        self.assertJSONEqual(str(self.client.get('/api/supplier/').content, encoding='utf-8'), [output, output2])

    def test_create(self):
        self.assertEquals(self.client.post('/api/supplier/', {'organisation': self.org, 'name': self.s_name, 'phone_number': self.s_pn}).status_code, 200)

    def test_read(self):
        self.assertJSONEqual(str(self.client.get('/api/supplier/1/').content, encoding="utf-8"), self.template)

    def test_partial_update(self):
        output = self.template
        self.assertEquals(self.client.patch('/api/supplier/1/', {"name":"new"}).status_code, 200)
        output["name"] = "new"
        self.assertJSONEqual(str(self.client.get('/api/supplier/1/').content, encoding="utf-8"), output)
        self.assertEquals(self.client.patch('/api/supplier/1/', {"phone_number":"000"}).status_code, 200)
        output["phone_number"] = "000"
        self.assertJSONEqual(str(self.client.get('/api/supplier/1/').content, encoding="utf-8"), output)

    def test_update(self):
        output = self.template
        self.assertEquals(self.client.put('/api/supplier/1/', {"name":"new", "phone_number":"000"}).status_code, 200)
        output["name"] = "new"
        output["phone_number"] = "000"
        self.assertJSONEqual(str(self.client.get('/api/supplier/1/').content, encoding="utf-8"), output)
    
    def test_invalid_inputs(self):
        self.assertEquals(self.client.patch('/api/supplier/1/', {"name":"x"*100}).status_code, 200)
        self.assertEquals(self.client.patch('/api/supplier/1/', {"name":"x"*101}).status_code, 400)
        self.assertEquals(self.client.patch('/api/supplier/1/', {"phone_number":"0"*11}).status_code, 400)
