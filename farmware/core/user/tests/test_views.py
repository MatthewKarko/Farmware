from django.http import HttpResponse

from rest_framework.test import APITestCase

import json

from ..models import User
from ...api.models.organisation import Organisation

import base64

TEST_USER_EMAIL = 'user@example.com'
TEST_ADMIN_EMAIL = 'admin@example.com'
STRONG_PASSWORD = 'qWejf-djjd3-$dksm'
FIELD_REQUIRED_RESPONSE = ["This field is required."]

CONTENT_TYPE = "application/json"

class UserViewSetTestCases(APITestCase):
    def setUp(self):
        org_code = '000000'

        self.organisation = Organisation.objects.create(
            code=org_code, name="Test Farm", logo="<logo>")

        # User details
        self.first_name = 'Johnny'
        self.last_name = 'Appleseed'
        self.email = 'johnnyappleseed@example.com'
        self.password = "password"

        self.user: User = User.objects.create_user(
            self.email, 
            self.first_name, 
            self.last_name, 
            self.organisation.code, 
            self.password)
        
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(f'{self.email}:{self.password}'.encode()).decode('ascii'),
        }

    def test_successful_register_new_user(self):
        """Test a successful user register."""
        payload = {
                 'email' : TEST_USER_EMAIL,
            'first_name' : 'first_name',
             'last_name' : 'last_name',
              'password' : STRONG_PASSWORD,
              'org_code' : self.organisation.code
            }

        response: HttpResponse = self.client.post(
            '/api/user/register/user/', 
            json.dumps(payload), 
            content_type=CONTENT_TYPE
            )

        self.assertEquals(response.status_code, 201)

        user: User = User.objects.get(**{'email': TEST_USER_EMAIL})
        # TODO: change this when TAG(EMAIL_CONFIRMATION) is activated
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff, "User should not be a staff.")
        self.assertFalse(user.is_superuser, "User should not be a superuser.")
        self.assertEqual(user.role, User.Roles.WORKER.value)

    def test_missing_fields_register_new_user(self):
        """Test an unsuccessful user register."""
        fields = ['first_name', 'last_name', 'org_code']
        
        for field in fields:
            self.run_missing_field_register_new_user(field)

    def run_missing_field_register_new_user(self, field: str):
        """Run the test for a missing field when registering a new user."""
        payload = {
                 'email' : TEST_USER_EMAIL,
            'first_name' : 'first_name',
             'last_name' : 'last_name',
              'password' : STRONG_PASSWORD,
              'org_code' : self.organisation.code
            }

        payload.pop(field)

        response: HttpResponse = self.client.post(
            '/api/user/register/user/', 
            json.dumps(payload), 
            content_type=CONTENT_TYPE
            )

        content = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertTrue(content.get(field, False) == FIELD_REQUIRED_RESPONSE)

    def test_weak_password_register_user(self):
        """
        Test creating a new user with weak passwords, i.e., too short, common,
        etc.
        """
        weak_passwords = [
            'password', 'mypassword', 'pw', 'admin', 'admin1'
            ]

        for password in weak_passwords:
            payload = {
                     'email' : TEST_USER_EMAIL,
                'first_name' : 'first_name',
                 'last_name' : 'last_name',
                  'password' : password,
                  'org_code' : self.organisation.code
                }

            response: HttpResponse = self.client.post(
                '/api/user/register/user/', 
                json.dumps(payload), 
                content_type=CONTENT_TYPE
                )

            self.assertEquals(response.status_code, 400)

    def test_register_user_org_code_does_not_exist(self):
        """Test creating a new user with a bad organisational code."""
        invalid_org_code = "111111"
        payload = {
            'email' : TEST_USER_EMAIL,
                'first_name' : 'first_name',
                 'last_name' : 'last_name',
                  'password' : STRONG_PASSWORD,
                  'org_code' : invalid_org_code
        }

        response: HttpResponse = self.client.post(
                '/api/user/register/user/', 
                json.dumps(payload), 
                content_type=CONTENT_TYPE
                )
        self.assertEquals(response.status_code, 406)

    def test_successful_register_admin(self):
        """Test a successful admin register."""
        payload = {
                 'email' : TEST_ADMIN_EMAIL,
            'first_name' : 'first_name',
             'last_name' : 'last_name',
              'password' : STRONG_PASSWORD,
              'org_name' : 'Test Organisation'
            }

        response: HttpResponse = self.client.post(
            '/api/user/register/admin/', 
            json.dumps(payload), 
            content_type=CONTENT_TYPE
            )

        self.assertEquals(response.status_code, 201)

        user: User = User.objects.get(**{'email': TEST_ADMIN_EMAIL})
        # TODO: change this when TAG(EMAIL_CONFIRMATION) is activated
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff, "Admin should not be a staff.")
        self.assertFalse(user.is_superuser, "Admin should not be a superuser.")
        self.assertEqual(user.role, User.Roles.ORGANISATION_ADMIN.value)        

    def test_weak_password_register_admin(self):
        """
        Test creating a new admin with weak passwords, i.e., too short, common,
        etc.
        """
        weak_passwords = [
            'password', 'mypassword', 'pw', 'admin', 'admin1'
            ]
        for password in weak_passwords:
            payload = {
                'email' : TEST_ADMIN_EMAIL,
                'first_name' : 'first_name',
                'last_name' : 'last_name',
                'password' : password,
                'org_name' : 'Test Organisation'
                }

            response: HttpResponse = self.client.post(
                '/api/user/register/admin/', 
                json.dumps(payload), 
                content_type=CONTENT_TYPE
                )

            self.assertEquals(response.status_code, 400)

    def test_register_admin_organisation_name_exists(self):
        """
        Test creating a new admin with a name that already exists. It should be
        okay.
        """
        # First register admin
        payload = {
            'email' : TEST_ADMIN_EMAIL,
            'first_name' : 'first_name',
            'last_name' : 'last_name',
            'password' : STRONG_PASSWORD,
            'org_name' : 'Test Organisation'
            }

        response: HttpResponse = self.client.post(
            '/api/user/register/admin/', 
            json.dumps(payload), 
            content_type=CONTENT_TYPE
            )

        self.assertEquals(response.status_code, 201)

        # Register admin of the same name (but different email)
        payload = {
            'email' : 'admin2@example.com',
            'first_name' : 'first_name',
            'last_name' : 'last_name',
            'password' : STRONG_PASSWORD,
            'org_name' : 'Test Organisation'
            }

        response: HttpResponse = self.client.post(
            '/api/user/register/admin/', 
            json.dumps(payload), 
            content_type=CONTENT_TYPE
            )

        self.assertEquals(response.status_code, 201)

    def test_set_password_successful(self):
        """Test setting the password of the user to a valid password."""
        payload = {
            'old_password' : self.password,
            'new_password' : STRONG_PASSWORD,
            }

        response: HttpResponse = self.client.post(
            f'/api/user/{self.user.pk}/set_password/', 
            json.dumps(payload), 
            content_type=CONTENT_TYPE,
            **self.auth_headers
            )

        self.assertEquals(response.status_code, 200)

    def test_set_password_unsuccessful(self):
        """Test setting the password of the user to something not valid."""
        payload = {
            'old_password' : self.password,
            'new_password' : self.password,
            }

        response: HttpResponse = self.client.post(
            f'/api/user/{self.user.pk}/set_password/', 
            json.dumps(payload), 
            content_type=CONTENT_TYPE,
            **self.auth_headers
            )

        self.assertEquals(response.status_code, 400)

    def test_removing_user(self):
        """
        Test destroying a user.

        You should not be able destroy other users outside your organisation 
        and if you are not an admin.
        """
        # TODO
        pass

    def test_list_users(self):
        """
        Test listing users.

        This should only list users within their organisation.
        Extra information should be displayed.
        """
        response: HttpResponse = self.client.get(
            f'/api/user/', 
            **self.auth_headers
            )

        self.assertEquals(response.status_code, 200)
        # TODO check the response of users is correct

    def test_getting_teams(self):
        """
        Test getting a user's teams.

        Should only return their teams. 
        """
        # TODO
        response: HttpResponse = self.client.get(
            f'/api/user/{self.user.pk}/teams/', 
            **self.auth_headers
            )

        self.assertEquals(response.status_code, 200)
        # TODO check the response of teams is correct

    def test_partial_updates(self):
        """
        Test partially updating user information.

        - A user TODO(verify this claim) should not be able to change their 
        password.
        - A user should not be able to change their role.
        - A user should not be able to change their organisation.
        """
        # TODO
        payload = {
            'password' : "new random !2312sad pwrod",
            }
        
        response: HttpResponse = self.client.patch(
            f'/api/user/{self.user.pk}/', 
            json.dumps(payload), 
            content_type=CONTENT_TYPE,
            **self.auth_headers
            )

        self.assertEquals(response.status_code, 200)