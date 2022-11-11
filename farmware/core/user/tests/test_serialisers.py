from django.test import TestCase

from ..models import User
from ..serialisers import (
    UserSerialiser, 
    UserUpdateSerialiser,
    LoginSerialiser,
    RegisterAdminSerialiser,
    RegisterUserSerialiser
)
from ...api.models.organisation import Organisation

# User details
FIRST_NAME = 'Johnny'
LAST_NAME = 'Appleseed'
EMAIL = 'johnnyappleseed@example.com'
PASSWORD = "password"

ORG_CODE = '000000'

ORGANISATION = dict(code=ORG_CODE, name="Test Farm", logo="<logo>")

class UserSerialiserTests(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(**ORGANISATION)

        self.user: User = User.objects.create_user(
            EMAIL, 
            FIRST_NAME, 
            LAST_NAME, 
            self.organisation.code, 
            PASSWORD)
        
        self.serialiser = UserSerialiser(self.user)

    def test_contains_expected_fields(self):
        """Ensure all fields are expected."""
        data = self.serialiser.data

        self.assertEqual(
            set(data.keys()), 
            set([ 'id','email','first_name', 'last_name','organisation', 
            'role', 'teams']
            )
        )

        # Password should not be seen, i.e., write_only = True
        with self.assertRaises(KeyError):
            data['password']

    def test_all_field_content(self):
        """Ensure all fields contain the correct information."""
        data = self.serialiser.data

        self.assertEqual(data['first_name'], FIRST_NAME)
        self.assertEqual(data['last_name'], LAST_NAME)
        self.assertEqual(data['email'], EMAIL)

        expected_role = {
            'level': self.user.role,
            'name': dict(User.Roles.choices)[self.user.role]
            }
        self.assertEqual(data['role'], expected_role)

        # TODO: teams


class UserUpdateSerialiserTests(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(**ORGANISATION)

        self.user: User = User.objects.create_user(
            EMAIL, 
            FIRST_NAME, 
            LAST_NAME, 
            self.organisation.code, 
            PASSWORD)

        self.serialiser = UserUpdateSerialiser(self.user)

    def test_contains_expected_fields(self):
        """Ensure all fields are expected."""
        data = self.serialiser.data

        self.assertEqual(
            set(data.keys()), 
            set([ 'id','email','first_name', 'last_name', 
            'role', 'teams']
            )
        )

        with self.assertRaises(KeyError):
            data['password']
            data['organisation']


class LoginSerialiserTests(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(**ORGANISATION)

        data = {
               'email' : EMAIL,
            'password' : PASSWORD,
            }

        self.serialiser = LoginSerialiser(data=data)  # type: ignore

    def test_contains_expected_fields(self):
        """Ensure all fields are expected."""
        self.assertTrue(self.serialiser.is_valid())


class RegisterAdminSerialiserTests(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(**ORGANISATION)

        data = {
                'first_name' : FIRST_NAME,
                 'last_name' : LAST_NAME,
                     'email' : EMAIL,
                  'password' : PASSWORD,
                  'org_name' : 'New Farm'
            }

        self.serialiser = RegisterAdminSerialiser(data=data)  # type: ignore

    def test_contains_expected_fields(self):
        """Ensure all fields are expected."""
        self.assertTrue(self.serialiser.is_valid())


class RegisterUserSerialiserTests(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(**ORGANISATION)

        data = {
                'first_name' : FIRST_NAME,
                 'last_name' : LAST_NAME,
                     'email' : EMAIL,
                  'password' : PASSWORD,
                  'org_code' : '800085'
            }

        self.serialiser = RegisterUserSerialiser(data=data)  # type: ignore

    def test_contains_expected_fields(self):
        """Ensure all fields are expected."""
        self.assertTrue(self.serialiser.is_valid())