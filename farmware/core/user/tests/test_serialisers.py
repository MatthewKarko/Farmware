from django.test import TestCase

from ..models import User
from ..serialisers import UserSerialiser
from ...api.models.organisation import Organisation

class UserSerialiserTests(TestCase):
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
        
        self.serialiser = UserSerialiser(self.user)

    def test_contains_expected_fields(self):
        """Ensure all fields are expected"""
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

        self.assertEqual(data['first_name'], self.first_name)
        self.assertEqual(data['last_name'], self.last_name)
        self.assertEqual(data['email'], self.email)

        expected_role = {
            'level': self.user.role,
            'name': dict(User.Roles.choices)[self.user.role]
            }
        self.assertEqual(data['role'], expected_role)

        # TODO: teams


# TODO:
# class UserUpdateSerialiserTests():
#     def setUp(self):
#         org_code=generate_random_org_code()
#         Organisation.objects.create(code=org_code,name="nameoforg", logo="logoofog")
#         Org=Organisation.objects.get(name="nameoforg")
#         response=Response()
#         response['email']='example@gmail.com'
#         response['first_name']='firstn'
#         response['last_name']='lastn'
#         response['password']='passwd'
#         response['organisation']=Org
#         response['role']=400
#         self.user=get_user_model().objects.create_user(email="email@gmail.com", first_name="first_name", last_name="last_name",organisation=Org,password="password123",role=400)
#         #self.user=get_user_model().objects.create_user(response)
#         #serializer=UserSerialiser(user)
#         #updatedSerializer=UserUpdateSerialiser()
#     def test_testingValidateRole(self):
#         #serializer=UserSerialiser(self.user)
#         #updatedSerializer=UserUpdateSerialiser(serializer,self.user)
#         #self.assertEquals(updatedSerializer.validate_role(10),"Illegal role allocation.")
#         #self.assertEquals(updatedSerializer.validate_role("any role"),"Role is not an option.")
#         #self.assertEquals(updatedSerializer.validate_role(1),1)
#         pass

# class LoginSerialiserTests():
#     def seUp(self):
#         org_code=generate_random_org_code()
#         Organisation.objects.create(code=org_code,name="nameoforg", logo="logoofog")
#         Org=Organisation.objects.get(name="nameoforg")
#         self.user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
#         self.serializer=UserSerialiser(self.user)
#         LoginSerialiser(self.serializer)
#     def testing_fields(self):
#         #user= get_user_model().objects.get(first_name="first_name")
#         #Org=Organisation.objects.get(name="nameoforg")
#         #serializer=UserSerialiser(user)
#         #raise ValueError(user.email)
#         ls = LoginSerialiser(self.serializer)
#         #ls=LoginSerialiser({'email':'email@gmail.com','password':'pass@123'})
#         #raise ValueError(ls.data)
#         #raise ValueError(ls)
#         raise ValueError(ls.data.keys())
#         ldata = ls.data
#         raise ValueError(ls.data.keys())
#         #raise ValueError(ldata)
#         self.assertEquals(ldata['email'],"email@gmail.com")
# class RegisterSerialiserTests():
#     def setUp(self):
#         org_code=generate_random_org_code()
#         Organisation.objects.create(code=org_code,name="nameoforg", logo="logoofog")
#         Org=Organisation.objects.get(name="nameoforg")
#         user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
#         serializer=UserSerialiser()
#         rs=RegisterSerialiser(serializer)
#     def testing_fields(self):
#         user=get_user_model().objects.get(first_name="first_name")
#         serializer=UserSerialiser(user)
#         rs=RegisterSerialiser(serializer)
#         data = rs.data
#         self.assertEquals(set(data.keys()),set( [
#             'first_name', 'last_name', 'password', 'email',
#         ],['id']))
# class RegisterUserSerialiserTests():
#     def setUp(self):
#         orgcode=generate_random_org_code()
#         Organisation.objects.create(code=orgcode,name="nameoforg", logo="logoofog")
#         Org=Organisation.objects.get(name="nameoforg")
#         self.user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
#         serializer=UserSerialiser(user)
#         rs=RegisterSerialiser(serializer)
#         rus=RegisterUserSerialiser(rs)
#     def test_testing_fields(self):
#         serializer=UserSerialiser(instance=self.User)
#         rs=RegisterSerialiser(serializer)
#         rus=RegisterUserSerialiser(rs)
#         data = self.rus.data
#         self.assertEquals(set(data.keys()),set( [
#             'first_name', 'last_name', 'password', 'email','org_name',
#         ],['id']))
#     def test_testing_create(self):
#         serializer=UserSerialiser()
#         rs=RegisterSerialiser(serializer)
#         rus=RegisterUserSerialiser(rs)
#         Org=Organisation.objects.get(name="nameoforg")
#         serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','organisation':Org}
#         rus.org_code=Org.code
#         self.assertIsNotNone(rus.create(serializer_data))