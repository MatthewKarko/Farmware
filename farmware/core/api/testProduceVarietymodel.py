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


class ProduceVarietyTestCases(TestCase):
    def setUp(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmo", logo="oat")
        organisatio = Organisation.objects.get(name="Farmo")
        produce = Produce.objects.create(organisation=organisatio, name="eggs")
        ProduceVariety.objects.create(produce_id=produce, variety="brown")

    def test_ProduceVariety(self):
        producevariety = ProduceVariety.objects.get(variety="brown")
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Faro", logo="oat")
        organisatio = Organisation.objects.get(name="Faro")
        produce2 = Produce.objects.create(
            organisation=organisatio, name="chicken")
        self.assertEqual(producevariety.variety, "brown")
        with self.assertRaises(ValidationError):
            ProduceVariety.objects.create(produce_id=produce2, variety="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean et justo ut turpis suscipit mattis ac ac lorem. Aenean molestie nisi et ullamcorper condimentum. Integer at congue nulla, quis elementum mauris. Mauris luctus nisl elementum massa vehicula, ut maximus purus pellentesque. Curabitur consectetur tincidunt malesuada. Sed dignissim ipsum nec urna tincidunt lobortis. Vestibulum porta finibus tincidunt. Nunc a odio porta, aliquam odio ut, commodo risus. Duis quis risus in nulla accumsan tempus dapibus et elit. Integer sed est at ligula commodo tristique.Sed et pulvinar mauris. Vivamus fringilla odio a ex porttitor, nec dapibus nisi vestibulum. Phasellus sed nisi velit. Vestibulum tempus justo dolor, et pellentesque urna molestie ut. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Curabitur viverra tincidunt hendrerit. Maecenas accumsan est vitae est faucibus facilisis. Sed nec quam in orci vehicula varius in ut urna. Proin lacus nibh, suscipit a elementum nec")
            raise ValidationError("error")
