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
# 0001_initial,0002_initial,0003_auto_20221018_0824,0004_auto_20221018_1055,0005_auto_20221018_1132
from .urls import *
from django_test_migrations.contrib.unittest_case import MigratorTestCase
from django.test import Client
from rest_framework.test import APITestCase


class AreaCodeTestCases(TestCase):
    def setUp(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmone", logo="goat")
        organisatio = Organisation.objects.get(name="Farmone")
        AreaCode.objects.create(
            organisation=organisatio, area_code="204", description="just another area code")

    def test_AreaCode1(self):
        areacodee = AreaCode.objects.get(area_code="204")
        self.assertEqual(areacodee.description, "just another area code")

    def test_AreaCode2(self):
        areacode = AreaCode.objects.get(area_code="204")
        with self.assertRaises(IntegrityError):
            AreaCode.objects.create(
                area_code="204", description="just another area code")

    def test_AreaCode3(self):
        #areacode = AreaCode.objects.get(area_code="204")
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmon", logo="got")
        organisatio = Organisation.objects.get(name="Farmon")
        with self.assertRaises(ValidationError):
            AreaCode.objects.create(organisation=organisatio, area_code="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque egestas, leo in mattis suscipit, ante arcu gravida sapien, sit amet varius quam mi vitae lectus. Nullam in aliquam odio. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In quis imperdiet purus. Curabitur quis laoreet tellus. Quisque gravida vitae arcu molestie interdum. Phasellus dictum urna est, ut feugiat turpis gravida sed. Pellentesque ut consectetur ante. Sed scelerisque mauris quis mi condimentum, a consectetur massa ullamcorper. Ut condimentum tellus ac lorem luctus ultrices. In nibh est, placerat ac dignissim sit amet, dapibus in libero. Quisque lobortis lacus et laoreet hendrerit. Quisque vel placerat mi. Suspendisse vitae sodales justo, sed dapibus sapien. Vestibulum bibendum fermentum fringilla. Aliquam vitae neque orci.Aenean euismod lacus id orci rutrum suscipit. In sit amet tortor vel mauris luctus lacinia. Suspendisse potenti. Mauris lorem sem, ornare in justo commodo, vulputate condimentum urna. Nam fermentum ipsum vestibulum vehicula cursus. Mauris iaculis ut risus a imperdiet. Suspendisse porttitor, sem sed laoreet luctus, est tellus bibendum felis, a dignissim justo velit a ante. Sed placerat justo eros, at viverra ex imperdiet aself.client. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec id odio nunself.client. Nulla tincidunt rhoncus tellus, sit amet maximus lectus blandit sit amet. Donec interdum vitae sapien sit amet varius. Proin imperdiet mauris eget cursus rhoncus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent id libero erat.Pellentesque gravida, lectus vitae porttitor dapibus, nisl nunc suscipit ante, eu varius sem dolor id ante. Pellentesque porta feugiat ipsum, eget pharetra dolor dapibus vitae. Donec gravida eleifend sem, ac dictum augue elementum eget. Ut accumsan maximus purus, sed aliquet tellus interdum vel. Praesent iaculis diam et neque rhoncus placerat. Mauris consectetur vel leo nec suscipit. Praesent placerat, felis facilisis.", description="ss")
            raise ValidationError("error")

    def test_AreaCode4(self):
        #areacode = AreaCode.objects.get(area_code="204")
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmon", logo="go")
        organisatio = Organisation.objects.get(name="Farmon")
        with self.assertRaises(ValidationError):
            AreaCode.objects.create(organisation=organisatio, area_code="203", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque egestas, leo in mattis suscipit, ante arcu gravida sapien, sit amet varius quam mi vitae lectus. Nullam in aliquam odio. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In quis imperdiet purus. Curabitur quis laoreet tellus. Quisque gravida vitae arcu molestie interdum. Phasellus dictum urna est, ut feugiat turpis gravida sed. Pellentesque ut consectetur ante. Sed scelerisque mauris quis mi condimentum, a consectetur massa ullamcorper. Ut condimentum tellus ac lorem luctus ultrices. In nibh est, placerat ac dignissim sit amet, dapibus in libero. Quisque lobortis lacus et laoreet hendrerit. Quisque vel placerat mi. Suspendisse vitae sodales justo, sed dapibus sapien. Vestibulum bibendum fermentum fringilla. Aliquam vitae neque orci.Aenean euismod lacus id orci rutrum suscipit. In sit amet tortor vel mauris luctus lacinia. Suspendisse potenti. Mauris lorem sem, ornare in justo commodo, vulputate condimentum urna. Nam fermentum ipsum vestibulum vehicula cursus. Mauris iaculis ut risus a imperdiet. Suspendisse porttitor, sem sed laoreet luctus, est tellus bibendum felis, a dignissim justo velit a ante. Sed placerat justo eros, at viverra ex imperdiet aself.client. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec id odio nunself.client. Nulla tincidunt rhoncus tellus, sit amet maximus lectus blandit sit amet. Donec interdum vitae sapien sit amet varius. Proin imperdiet mauris eget cursus rhoncus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent id libero erat.Pellentesque gravida, lectus vitae porttitor dapibus, nisl nunc suscipit ante, eu varius sem dolor id ante. Pellentesque porta feugiat ipsum, eget pharetra dolor dapibus vitae. Donec gravida eleifend sem, ac dictum augue elementum eget. Ut accumsan maximus purus, sed aliquet tellus interdum vel. Praesent iaculis diam et neque rhoncus placerat. Mauris consectetur vel leo nec suscipit. Praesent placerat, felis facilisis.")
            raise ValidationError("error")
