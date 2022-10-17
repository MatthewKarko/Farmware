from django.test import TestCase
from .models import *
from .views import ActivateAccount,BlacklistTokenUpdateView,CurrentUserView
from ..api.models.organisation import Organisation
from rest_framework import serializers, exceptions
from rest_framework import status
from rest_framework.test import APITestCase
#from .urls import *
#from rest_framework.routers import DefaultRouter
from django.test import Client

# Create your tests here.
class UserManagerTestCases(TestCase):
    def set_up(self):
        Organisation.objects.create(name="nameoforg", logo="logoofog")
    def test_create_user(self):
        organisation= Organisation.objects.get(name="nameoforg")
        user=UserManager.create_user("email@gmail.com", "first_name", "last_name", organisation, None)
        self.assertEqual(user.email, "email@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    def test_create_user_is_staff(self):
        user=UserManager.create_user("email@gmail.com", "first_name", "last_name", organisation, None)
        self.assertEqual(user.email, "email@gmail.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
    def test_create_superuser(self):
        user=UserManager.create_user("email@gmail.com", "first_name", "last_name", organisation, "password")
        self.assertEqual(user.email, "email@gmail.com")
        self.assertTrue(user.password, "password")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

class UserSerialiserTests(self):
    def set_up(self):
        Organisation.objects.create(name="nameoforg", logo="logoofog")
        Org=Orgaisation.objects.get(name="nameoforg")
        self.User=UserManager.create_user("email@gmail.com", "first_name", "last_name", Org, 3,"password123")
        self.serializer=UserSerialiser(instance=self.User)

    def test_contains_expected_fields(self):
        data=self.serializer.data
         self.assertItemsEqual(set(data.keys()), set([
             'id',
             'email',
             'first_name', 'last_name', 'password',
             'organisation', 'role', 'teams'
         ],['created', 'updated']))

    def test_all_the_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['first_name'], "first_name")
        self.assertEqual(data['last_name'], "last_name")
        self.assertEqual(data['password'], "password123")
        self.assertEqual(data['email'], "email@gmail.com")

class UserUpdateSerialiserTests(self):
    def set_up(self):
        Organisation.objects.create(name="nameoforg", logo="logoofog")
        Org=Orgaisation.objects.get(name="nameoforg")
        User=UserManager.create_user("email@gmail.com", "first_name", "last_name", Org, 3,"password123")
        serializer=UserSerialiser(instance=self.User)
        updatedSerializer=UserUpdateSerializer(self.serializer)
  def testingValidateRole(self):
      self.assertEquals(updatedSerializer.validate_role(10),"Illegal role allocation.")
      self.assertEquals(updatedSerializer.validate_role("any role"),"Role is not an option.")
      self.assertEquals(updatedSerializer.validate_role(1),1)

class LoginSerialiserTests(self):
    def set_up(self):
        Organisation.objects.create(name="nameoforg", logo="logoofog")
        Org=Orgaisation.objects.get(name="nameoforg")
        User=UserManager.create_user("email@gmail.com", "first_name", "last_name", Org, 3,"password123")
        serializer=UserSerialiser(instance=self.User)
        ls=LoginSerialiser(serializer)
    def testing_fields(self):
        data = self.ls.data
        self.assertEquals(data.keys(), ['email', 'password'])
class RegisterSerialiserTests(self):
    def set_up(self):
        Organisation.objects.create(name="nameoforg", logo="logoofog")
        Org=Orgaisation.objects.get(name="nameoforg")
        User=UserManager.create_user("email@gmail.com", "first_name", "last_name", Org, 3,"password123")
        serializer=UserSerialiser(instance=self.User)
        rs=RegisterSerialiser(serializer)
    def testing_fields(self):
        data = self.rs.data
        self.assertEquals(set(data.keys()),set( [
            'first_name', 'last_name', 'password', 'email',
        ],['id']))
class RegisterUserSerialiserTests(self):
    def set_up(self):
        Organisation.objects.create(name="nameoforg", logo="logoofog")
        Org=Orgaisation.objects.get(name="nameoforg")
        User=UserManager.create_user("email@gmail.com", "first_name", "last_name", Org, 3,"password123")
        serializer=UserSerialiser(instance=self.User)
        rs=RegisterSerialiser(serializer)
        rus=RegisterUserSerialiser(rs)
    def testing_fields(self):
        data = self.rus.data
        self.assertEquals(set(data.keys()),set( [
            'first_name', 'last_name', 'password', 'email','org_name',
        ],['id']))
    def testing_create(self):
        serializer_data = {
         'email': 'example@gmail.com',
         'first_name':'firstn',
         'last_name':'lastn',
         'password':'passwd',
         'organisation':org
       }
       self.assertNotNull(rus.create(serializer_data))
class UserViewSetTest(self):
    def set_up(self):
        Organisation.objects.create(name="nameoforg", logo="logoofog")
        c = Client()
    def testRegisteringUser(self):
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {
         'email': 'example@gmail.com',
         'first_name':'firstn',
         'last_name':'lastn',
         'password':'passwd',
         'organisation':org
       }
        response=c.post(reverse('register/user'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
    def testRegisteringUserError(self):
        response=c.post(reverse(register/user),{
        })
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
    def testRegisteringAdmin(self):
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {
         'email': 'example@gmail.com',
         'first_name':'firstn',
         'last_name':'lastn',
         'password':'passwd',
         'organisation':org,
         'role':000
       }
        response=c.post(reverse('register/admin'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
    def  testRegisteringAdminError(self):
        serializer_data={}
        response=c.post(reverse('register/admin'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
    def testingSettingPasswordsError(self):
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {
         'email': 'example@gmail.com',
         'first_name':'firstn',
         'last_name':'lastn',
         'password':'passwd',
         'organisation':org
       }
       response=c.post(reverse(''),serializer_data)
      self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
    def testingSettingPasswordsError2(self):
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {
         'email': 'example@gmail.com',
         'first_name':'firstn',
         'last_name':'lastn',
         'password':'passwd',
         'organisation':org,
         'old_password':'',
         'new_password':''
       }
       response=c.post(reverse('register/user'),serializer_data)
       self.assertEquals(response.status_code,status.HTTP_201_CREATED)
       user=User.objects.get(first_name="firstn")
       response=c.post(reverse(''),serializer_data,user.id)
      self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
    def testingSettingPasswords(self):
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {
         'email': 'example@gmail.com',
         'first_name':'firstn',
         'last_name':'lastn',
         'password':'passwd',
         'organisation':org,
         'old_password':'pass',
         'new_password':'passwpr'
       }
       response=c.post(reverse('register/user'),serializer_data)
       self.assertEquals(response.status_code,status.HTTP_201_CREATED)
       user=User.objects.get(first_name="firstn")
       response=c.post(reverse(''),serializer_data,user.id)
      self.assertEquals(response.status_code,status.HTTP_200_OK)
    def testingDestroy(self):
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {
         'email': 'example@gmail.com',
         'first_name':'firstn',
         'last_name':'lastn',
         'password':'passwd',
         'organisation':org
       }
       response=c.post(reverse('register/user'),serializer_data)
       self.assertEquals(response.status_code,status.HTTP_201_CREATED)

        response=c.post(reverse("destroy"),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_200_OK)
    def testingList(self):
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {
         'email': 'example@gmail.com',
         'first_name':'firstn',
         'last_name':'lastn',
         'password':'passwd',
         'organisation':org
       }
       response=c.post(reverse('register/user'),serializer_data)
       self.assertEquals(response.status_code,status.HTTP_201_CREATED)

       repsonse=c.get(reverse('list'),serializer_data)
       self.assertNotEquals(response,Null)

    def testingpermissionsInvalid(self):
        response= c.get(reverse(),{})
        self.assertEquals(response,[])
    def testingPermissionValid(self):
        rg= Organisation.objects.get(name="nameoforg")
        serializer_data = {
         'email': 'example@gmail.com',
         'first_name':'firstn',
         'last_name':'lastn',
         'password':'passwd',
         'organisation':org,
         'role':000
       }
        response=c.post(reverse('register/admin'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        response= c.get(reverse(get_permissions))
        self.assertEquals(response,[AllowAny()])

class ActivateAccountTests(self):
    def set_up(self):
        c =Client()
        TokenGenerator tg=TokenGenerator()
        Organisation.objects.create(name="nameoforg", logo="logoofog")
    def testingGet(self):
        Org=Orgaisation.objects.get(name="nameoforg")
        user=UserManager.create_user("email@gmail.com", "first_name", "last_name", Org, 3,"password123")
        tg._make_hash_value(user, timestamp)
        response = c.get('activate/<uidb64>/<token>',request, uidb64, token')
