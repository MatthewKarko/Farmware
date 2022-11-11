from django.test import TestCase
from ..models import *
from django.core.exceptions import ValidationError

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
