# TODO

from django.db import IntegrityError, transaction
from django.test import Client, TestCase

from rest_framework import serializers, exceptions
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient

from ..models import User
from ..serialisers import UserSerialiser
from ...api.models.organisation import Organisation


class BlacklistTokenUpdateViewTestCases(TestCase):
    def setUp(self) -> None:
        org_code = "000000"

        self.organisation = Organisation.objects.create(
            code=org_code, name="Test Farm", logo="<logo>")

    def test_testingPostError(self):
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        tg=TokenGenerator()
        c=Client()
        timestamp =time.time()
        token=tg._make_hash_value(user, timestamp)
        request={'refresh_token':token}
        response = c.post('logout/blacklist/',request)
        self.assertEquals(response.status_code,404)
        
    def test_posting(self):
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        tg=TokenGenerator()
        c=Client()
        token = account_activation_token
        request={'refresh_token':token}
        response = c.post('logout/blacklist/',request)
        self.assertEquals(response.status_code,404)