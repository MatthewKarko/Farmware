from django.test import TestCase
from ..models import *
# from django.core.exceptions import ValidationError
from django.db import IntegrityError

class TeamTestCases(TestCase):
    def setUp(self):
        organisation=Organisation.objects.create(name="Farmone",logo="goat")
        Team.objects.create(category ="j",name = "jack",organisation = organisation)

    # Test Team fields are correct
    def test_team_fields(self):
        cat = Team.objects.get(category="j")
        self.assertEqual(cat.category, "j")
        self.assertEquals(cat.name,"jack")
    

    # Test Team raises error if same name & category is used again.
    def test_team_repeat_integrity_error(self):
        org = Organisation.objects.get(name="Farmone")
        with self.assertRaises(IntegrityError):
            Team.objects.create(category ="j",name = "jack",organisation = org)

    # Test that multiple Teams can be added to an organisation
    def test_team_multiple(self):
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farm2", logo="go")
        org = Organisation.objects.get(code=org_code)
        Team.objects.create(category ="j123",name = "jack",organisation = org)
        Team.objects.create(category ="b123",name = "bob",organisation = org)
        self.assertEqual(Team.objects.get(
            category="j123").name, "jack")
        self.assertEqual(Team.objects.get(
            category="b123").name, "bob")