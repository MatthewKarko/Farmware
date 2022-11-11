from rest_framework.test import APITestCase

from ..models import User
from ...api.models.organisation import Organisation


class ActivateAccountTestCases(APITestCase):
    def setUp(self) -> None:
        org_code = "000000"

        self.organisation = Organisation.objects.create(
            code=org_code, name="Test Farm", logo="<logo>")

    # TODO