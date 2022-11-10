# TODO

from django.db import IntegrityError, transaction
from django.test import Client, TestCase

from rest_framework import serializers, exceptions
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient

from ..models import User
from ..serialisers import UserSerialiser
from ...api.models.organisation import Organisation


class ActivateAccountTestCases(APITestCase):
    def setUp(self) -> None:
        org_code = "000000"

        self.organisation = Organisation.objects.create(
            code=org_code, name="Test Farm", logo="<logo>")

    def test_testingGet(self):
        #user = User.objects.first()
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        self.client.force_authenticate(user)
        tg=TokenGenerator()
        request ={'user':user}
        timestamp =time.time()
        uidb64 = urlsafe_base64_encode(user.pk.to_bytes(5,'big'))
        token=tg._make_hash_value(user, timestamp)
        respons=self.client.post(f'/api/user/ /activate/{uidb64}/{token}/',{'user':user})
        self.assertEquals(respons.status_code,200)

    def test_testingGetError1(self):
        c =Client()
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        tg=TokenGenerator()
        request ={'user':user}
        timestamp =time.time()
        uidb64 =None
        token=tg._make_hash_value(user, timestamp)
        response = c.get('activate/<uidb64>/<token>',request, uidb64, token)
        self.assertEquals(response.status_code,404)
        
    def test_testingGetError2(self):
        c =Client()
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        tg=TokenGenerator()
        request ={'user':user}
        timestamp =time.time()
        uidb64 = urlsafe_base64_encode(user.pk.to_bytes(5,'big'))
        token=None
        response = c.get('activate/<uidb64>/<token>',request, uidb64, token)
        self.assertEquals(response.status_code,404)