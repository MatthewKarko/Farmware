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

class TeamTestCases(TestCase):
    def setUp(self):
        organisation=Organisation.objects.create(name="Farmone",logo="goat")
        Team.objects.create(category ="j",name = "jack",organisation = organisation)
    def test_Team(self):
        team=Team.objects.get(category ="j")
        self.assertEqual(team.name,"jack")
        organisation2=Organisation.objects.create(name="Farmon",logo="goa")
        with self.assertRaises(ValidationError):
            Team.objects.create(category ="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis euismod gravida. Vestibulum quam lacus, faucibus ac dui nec, hendrerit lobortis arcu. Ut vel lorem at enim dignissim porttitor in nec neque. Mauris lobortis justo lorem, id venenatis dui laoreet vel. Quisque egestas neque quis erat porttitor fermentum. Proin cursus, lorem non auctor aliquam, turpis neque tincidunt sem, vitae maximus massa dolor ut diam. Nam euismod urna sed leo vestibulum ultrices. Donec tempus fringilla feugiat. Nullam faucibus mattis diam, in sagittis lacus aliquam eget. Mauris eu ligula fermentum, bibendum enim id, sodales turpis. Praesent sed risus felis. Vivamus ut ultrices nisl.Ut luctus purus neque, eget blandit augue consectetur at. Etiam eleifend cursus tortor, ut venenatis lectus laoreet sollicitudin. Nunc at elementum magna. Integer ut scelerisque arcu, ac pellentesque lorem. Donec rutrum porttitor consectetur. Nunc nunc enim, sollicitudin mollis maximus non, lacinia at neque. Curabitur ultrices tincidunt pharetra. Vestibulum vitae.",name = "jack",organisation = organisation2)
            raise ValidationError("error")
    def test_team2(self):
        organisation2=Organisation.objects.create(name="Farmon",logo="goa")
        with self.assertRaises(ValidationError):
            Team.objects.create(category ="Jack",name = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis euismod gravida. Vestibulum quam lacus, faucibus ac dui nec, hendrerit lobortis arcu. Ut vel lorem at enim dignissim porttitor in nec neque. Mauris lobortis justo lorem, id venenatis dui laoreet vel. Quisque egestas neque quis erat porttitor fermentum. Proin cursus, lorem non auctor aliquam, turpis neque tincidunt sem, vitae maximus massa dolor ut diam. Nam euismod urna sed leo vestibulum ultrices. Donec tempus fringilla feugiat. Nullam faucibus mattis diam, in sagittis lacus aliquam eget. Mauris eu ligula fermentum, bibendum enim id, sodales turpis. Praesent sed risus felis. Vivamus ut ultrices nisl.Ut luctus purus neque, eget blandit augue consectetur at. Etiam eleifend cursus tortor, ut venenatis lectus laoreet sollicitudin. Nunc at elementum magna. Integer ut scelerisque arcu, ac pellentesque lorem. Donec rutrum porttitor consectetur. Nunc nunc enim, sollicitudin mollis maximus non, lacinia at neque. Curabitur ultrices tincidunt pharetra. Vestibulum vitae.",organisation = organisation2)
            raise ValidationError("error")
