from django.db import IntegrityError, transaction
from django.test import TestCase

from ..models import User
from ...api.models.organisation import Organisation

# Create your tests here.
class UserManagerTestCases(TestCase):
    organisation: Organisation

    def setUp(self) -> None:
        org_code = "000000"

        self.organisation = Organisation.objects.create(
            code=org_code, name="Test Farm", logo="<logo>")

    def test_create_user(self):
        """Test creating a normal user."""

        # User details
        first_name = 'Johnny'
        last_name = 'Appleseed'
        email = 'johnnyappleseed@example.com'
        password = "password"

        user: User = User.objects.create_user(
            email, 
            first_name, 
            last_name, 
            self.organisation.code, 
            password)

        # Basic assertions
        self.assertEqual(user.email, email, "'email' does not match.")
        self.assertEqual(user.first_name, first_name, "'first_name' does not match.")
        self.assertEqual(user.last_name, last_name, "'last_name' does not match.")
        self.assertNotEqual(user.password, password, "password should be hashed.")
        self.assertTrue(user.check_password(password), "password should be hashed.")

        # Other assertions
        # TODO: change this when TAG(EMAIL_CONFIRMATION) is activated
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff, "User should not be a staff.")
        self.assertFalse(user.is_superuser, "User should not be a superuser.")
        self.assertEqual(user.role, User.Roles.WORKER.value)
        self.assertEqual(user.teams.count(), 0)

    def test_create_user_errors(self):
        """Test creating a normal user with errors."""
        # User details
        first_name = 'Johnny'
        last_name = 'Appleseed'
        email = 'johnnyappleseed@example.com'
        password = "password"

        User.objects.create_user(
            email, 
            first_name, 
            last_name, 
            self.organisation.code, 
            password)

        with transaction.atomic():
            # Try add the same person
            with self.assertRaises(IntegrityError):
                User.objects.create_user(
                    email, 
                    first_name, 
                    last_name, 
                    self.organisation.code, 
                    password)

        with transaction.atomic():    
            with self.assertRaises(IntegrityError):
                User.objects.create_user(
                    email, 
                    "different first_name", 
                    last_name, 
                    self.organisation.code, 
                    password)

        with transaction.atomic():    
            with self.assertRaises(IntegrityError):
                User.objects.create_user(
                    email, 
                    first_name, 
                    "different last_name", 
                    self.organisation.code, 
                    password)

        with transaction.atomic():    
            different_organisation = Organisation.objects.create(
            code='111111', name="Test Farm Two", logo="<logo>")

            # Different org code should still raise an error
            with self.assertRaises(IntegrityError):
                User.objects.create_user(
                    email, 
                    first_name, 
                    last_name, 
                    different_organisation,
                    password)