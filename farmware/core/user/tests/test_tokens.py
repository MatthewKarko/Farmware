from django.db import IntegrityError, transaction
from django.test import Client, TestCase

from rest_framework import serializers, exceptions
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient

from ..models import User
from ..serialisers import UserSerialiser
from ...api.models.organisation import Organisation
from ..tokens import TokenGenerator

import time


class BlacklistTokenUpdateViewTestCases(TestCase):
    def setUp(self) -> None:
        org_code = "000000"

        self.organisation = Organisation.objects.create(
            code=org_code, name="Test Farm", logo="<logo>")

    # TODO