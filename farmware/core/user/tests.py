from django.test import TestCase
from .models import *
from .views import ActivateAccount,BlacklistTokenUpdateView,CurrentUserView
#from ..api.models.organisation import *
#from ..api.models import *
from .serialisers import *
from core.api.models.organisation import *
from rest_framework import serializers, exceptions
from rest_framework import status
from rest_framework.test import APITestCase
from .urls import *
#from rest_framework.routers import DefaultRouter
from django.test import Client
from django.contrib.auth import get_user_model
import time
from django.urls import reverse
from .tokens import *
from .viewsets import *
# Create your tests here.
class UserManagerTestCases(TestCase):
    def setUp(self):
        pass
    def test_create_user(self):
        #org_code=generate_random_org_code()
        org_code="abcdef"
        Organisation.objects.create(code =org_code,name="nameoforg", logo="logoofog")
        organisation= Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", org_code, None)
        self.assertEqual(user.email, "email@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    def test_create_user_is_staff(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code =org_code,name="nameoforg", logo="logoofog")
        organisation= Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", org_code, None,is_staff=True)
        self.assertEqual(user.email, "email@gmail.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
    def test_create_superuser(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code =org_code,name="nameoforg", logo="logoofog")
        organisation= Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_superuser("email@gmail.com", "first_name", "last_name", org_code)
        self.assertEqual(user.email, "email@gmail.com")
        self.assertTrue(user.password, "password")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class UserSerialiserTests(TestCase):
    def setUp(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code=org_code,name="nameoforg", logo="logoofog")
        Org=Organisation.objects.get(name="nameoforg")
        self.user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org)
        self.serializer=UserSerialiser(self.user)

    def test_contains_expected_fields(self):
        data=self.serializer.data
        self.assertEqual(set(data.keys()), set([ 'id','email','first_name', 'last_name','organisation', 'role', 'teams']))

    def test_all_the_field_content(self):
        data = self.serializer.data
    #    raise ValueError(data)
        self.assertEqual(data['first_name'], "first_name")
        self.assertEqual(data['last_name'], "last_name")
        #self.assertEqual(data['password'], "password123")
        self.assertEqual(data['email'], "email@gmail.com")

class UserUpdateSerialiserTests(TestCase):
    def setUp(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code=org_code,name="nameoforg", logo="logoofog")
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        serializer=UserSerialiser()
        updatedSerializer=UserUpdateSerialiser()
    def test_testingValidateRole(self):
        self.assertEquals(updatedSerializer.validate_role(10),"Illegal role allocation.")
        self.assertEquals(updatedSerializer.validate_role("any role"),"Role is not an option.")
        self.assertEquals(updatedSerializer.validate_role(1),1)

class LoginSerialiserTests(TestCase):
    def setUp(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code=org_code,name="nameoforg", logo="logoofog")
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        serializer=UserSerialiser()
        ls=LoginSerialiser(serializer)
    def test_testing_fields(self):
        user= get_user_model().objects.get(first_name="first_name")
        Org=Organisation.objects.get(name="nameoforg")
        serializer=UserSerialiser(user)
        #raise ValueError(user.email)
        ls = LoginSerialiser(serializer)
        #ls=LoginSerialiser({'email':'email@gmail.com','password':'pass@123'})
        #raise ValueError(ls.data)
        #data = ls.data
        self.assertEquals(ls.data['email'],"email@gmail.com")
class RegisterSerialiserTests(TestCase):
    def setUp(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code=org_code,name="nameoforg", logo="logoofog")
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        serializer=UserSerialiser()
        rs=RegisterSerialiser(serializer)
    def test_testing_fields(self):
        user=get_user_model().objects.get(first_name="first_name")
        serializer=UserSerialiser(user)
        rs=RegisterSerialiser(serializer)
        data = rs.data
        self.assertEquals(set(data.keys()),set( [
            'first_name', 'last_name', 'password', 'email',
        ],['id']))
class RegisterUserSerialiserTests(TestCase):
    def setUp(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code=org_code,name="nameoforg", logo="logoofog")
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        serializer=UserSerialiser()
        rs=RegisterSerialiser(serializer)
        rus=RegisterUserSerialiser(rs)
    def test_testing_fields(self):
        serializer=UserSerialiser(instance=self.User)
        rs=RegisterSerialiser(serializer)
        rus=RegisterUserSerialiser(rs)
        data = self.rus.data
        self.assertEquals(set(data.keys()),set( [
            'first_name', 'last_name', 'password', 'email','org_name',
        ],['id']))
    def test_testing_create(self):
        Org=Organisation.objects.get(name="nameoforg")
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','organisation':org}
        self.assertNotNull(rus.create(serializer_data))

class UserViewSetTestCases(TestCase):
    def setUp(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code=org_code,name="nameoforg", logo="logoofog")
        Org= Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        c = Client()
    def test_testRegisteringUser(self):
        c = Client()
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = { 'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','organisation':org}
        response=c.post(reverse('user-register-user',args=serializer_data))
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #raise ValueError(router.urls)
    def test_RegisteringUserError(self):
        c = Client()
        response=c.post(reverse('register/user'),{
        })
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
    def test_RegisteringAdmin(self):
        c = Client()
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {
         'email': 'example@gmail.com',
         'first_name':'firstn',
         'last_name':'lastn',
         'password':'passwd',
         'organisation':org,
         'role':000
       }
        response=c.post(reverse('register--admin'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
    def  test_RegisteringAdminError(self):
        c = Client()
        serializer_data={}
        response=c.post(reverse('register/admin'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
    def test_estingSettingPasswordsError(self):
        c = Client()
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
    def test_testingSettingPasswordsError2(self):
        c = Client()
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','organisation':org,'old_password':'','new_password':''}
        response=c.post(reverse('register/user'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        user=User.objects.get(first_name="firstn")
        response=c.post(reverse(''),serializer_data,user.id)
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
    def test_testingSettingPasswords(self):
        c = Client()
        org= Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.get(first_name="first_name")
        serializer_data = {'email': 'example@gmail.com','first_name':'first_name','last_name':'last_name','password':'passwd','organisation':org,'old_password':'pass','new_password':'passwpr'}
        f=UserViewSet()
        raise ValueError(urlpatterns)
        ur=reverse('user:user-set-password',args=[serializer_data],kwargs={'pk': user.pk})
        raise ValueError(ur)
        response=c.post(reverse('user:user-set-pasword',args=[serializer_data]))
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        user=User.objects.get(first_name="firstn")
        response=c.post(reverse((''),args=[serializer_data,user.id]))
        self.assertEquals(response.status_code,status.HTTP_200_OK)
    def test_testingDestroy(self):
        c = Client()
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','organisation':org}
        response=c.post(reverse('register/user'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        response=c.post(reverse("destroy"),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_200_OK)
    def test_testingList(self):
        c = Client()
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','organisation':org}
        response=c.post(reverse('register/user'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        repsonse=c.get(reverse('list'),serializer_data)
        self.assertNotEquals(response,Null)
    def test_testingpermissionsInvalid(self):
        c = Client()
        response= c.get(reverse(),{})
        self.assertEquals(response,[])
    def test_testingPermissionValid(self):
        c = Client()
        org= Organisation.objects.get(name="nameoforg")
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','organisation':org,'role':000}
        response=c.post(reverse('register/admin'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        response= c.get(reverse(get_permissions))
        self.assertEquals(response,[AllowAny()])
    def test_testingMyteams(self):
        c= Client()
        org= Organisation.objects.get(name="nameoforg")
        team=Team.objects.create(category="sports",name="fifa team 12",organisation=org)
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','organisation':org,'role':000,'team':team}
        response=c.post(reverse('register/admin'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        s_data={
        'user':user
        }
        response2 = c.post(reverse('teams',args=s_data))
        self.assertEquals(response2.status,200)
    def test_testingUserteams(self):
        c= Client()
        org= Organisation.objects.get(name="nameoforg")
        team=Team.objects.create(category="sports",name="fifa team 12",organisation=org)
        serializer_data = {'email': 'example@gmail.com','first_name':'firstn','last_name':'lastn','password':'passwd','organisation':org,'role':000,'team':team}
        response=c.post(reverse('register/admin'),serializer_data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        s_data={
        'user':user
        }
        response2 = c.post(reverse('teams',args=[s_data,user.pk]))
        self.assertEquals(response2.status,200)


class ActivateAccountTestCases(TestCase):
    def setUp(self):
        c =Client()
        org_code=generate_random_org_code()
        Organisation.objects.create(code=org_code,name="nameoforg", logo="logoofog")
    def test_testingGet(self):
        c =Client()
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        tg=TokenGenerator()
        request ={'user':user}
        timestamp =time.time()
        uidb64 = urlsafe_base64_encode(user.pk.to_bytes(5,'big'))
        token=tg._make_hash_value(user, timestamp)
        response = c.get('activate/<uidb64>/<token>',request, uidb64, token)
        #raise ValueError(response)
        self.assertEquals(response.status_code,201)
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
class BlacklistTokenUpdateViewTestCases(TestCase):
    def setUp(self):
        org_code=generate_random_org_code()
        Organisation.objects.create(code=org_code,name="nameoforg", logo="logoofog")
    def test_testingPostError(self):
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        tg=TokenGenerator()
        c=Client()
        timestamp =time.time()
        token=tg._make_hash_value(user, timestamp)
        request={'refresh_token':token}
        response = c.post('logout/blacklist/',request)
        self.assertEquals(response.status_code,404)
    def test_posting(self):
        Org=Organisation.objects.get(name="nameoforg")
        user=get_user_model().objects.create_user("email@gmail.com", "first_name", "last_name", Org,"password123")
        tg=TokenGenerator()
        c=Client()
        token = account_activation_token
        request={'refresh_token':token}
        response = c.post('logout/blacklist/',request)
        self.assertEquals(response.status_code,404)
