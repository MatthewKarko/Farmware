from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ..models import *

#Test the Customer API endpoints using create_user permission levels.
class CustomerViewsetTestCases(APITestCase):
    def setUp(self):
        #Create an organisation
        org_code = generate_random_org_code()
        Organisation.objects.create(code=org_code, name="Farmone", logo="goat")

    # Test creation of customer using POST to /api/customer/ endpoint
    def test_creating(self):
        organisation = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisation.code, None, is_staff=True)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/api/customer/', {'name': 'ralph', 'phone_number': '9170002894'})
        self.assertEquals(response.status_code, 200)

        #check was added correctly
        self.assertEquals(Customer.objects.get(name="ralph").phone_number,"9170002894")

    #Tests that multiple customers can be created in an organisation
    def test_create_multiple(self):
        organisation = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisation.code, None, is_staff=True)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/api/customer/', {'name': 'ralph', 'phone_number': '9170002894'})
        self.assertEquals(response.status_code, 200)
        response2 = self.client.post(
            '/api/customer/', {'name': 'bob', 'phone_number': '1231231231'})
        self.assertEquals(response2.status_code, 200)
        self.assertEquals(Customer.objects.get(name="ralph").phone_number,"9170002894")
        self.assertEquals(Customer.objects.get(name="bob").phone_number,"1231231231")

    #Tests that customers can be deleted
    def test_destroy(self):
        organisation = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisation.code, None, is_staff=True)
        self.client.force_authenticate(user)

        response = self.client.post(
            '/api/customer/', {'organisation': organisation, 'name': 'ralph', 'phone_number': '9170002894'})
        self.assertEquals(response.status_code, 200)

        #get the id of customer created
        customer_id = Customer.objects.get(name="ralph").id

        response2 = self.client.delete(f'/api/customer/'+str(customer_id)+"/")
        self.assertEquals(response2.status_code, 200)

        #check ralph doesn't exist
        self.assertRaises(Customer.DoesNotExist, Customer.objects.get, name="ralph")

    # Test partially updating customer works using PATCH to /api/customer/{id}/ endpoint
    def test_partial_update(self):
        # setup the user
        organisation = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisation.code, None, is_staff=True)
        self.client.force_authenticate(user)

        #create the customer will modify
        response = self.client.post(
            '/api/customer/', {'name': 'bobbyb', 'phone_number': '1234123412'})
        self.assertEquals(response.status_code, 200)
        
        # Get the id of the area code created
        customer_id = Customer.objects.get(name="bobbyb").id

        #modify the customer
        patch_response = self.client.patch('/api/customer/'+str(customer_id)+'/', {'phone_number': "0123456789"})
        self.assertEquals(patch_response.status_code, 200)

        #check it did change
        self.assertEquals(Customer.objects.get(name="bobbyb").phone_number,"0123456789")

    # Test updating customer works using PUT to /api/customer/{id}/ endpoint
    def test_update(self):
        #setup the user
        organisation = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisation.code, None, is_staff=True)
        self.client.force_authenticate(user)

        #create the customer to update
        response = self.client.post(
            '/api/customer/', {'organisation': organisation, 'name': 'bobbybc', 'phone_number': '9170002894'})
        self.assertEquals(response.status_code, 200)

        #get added customer ID
        customer_id = Customer.objects.get(name="bobbybc").id

        #make put request
        put_response = self.client.put('/api/customer/'+str(customer_id)+'/', {'name': 'bobbybc','phone_number': "12312312"})
        self.assertEquals(put_response.status_code, 200)

        # Check it updated
        self.assertEquals(Customer.objects.get(name="bobbybc").phone_number,"12312312")

    # Test listing all of the customers using GET /api/customer/ endpoint
    def test_list(self):
        organisation = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisation.code, None, is_staff=True)
        self.client.force_authenticate(user)

        #create 2 customers
        response = self.client.post(
            '/api/customer/', {'organisation': organisation, 'name': 'bobbybc', 'phone_number': '9170002894'})

        response = self.client.post(
            '/api/customer/', {'organisation': organisation, 'name': 'bill', 'phone_number': '12312312'})

        get_response = self.client.get('/api/customer/')
        self.assertEquals(get_response.status_code,200)

        #Convert response to json
        json_response = get_response.json()

        #check the json response is correct
        self.assertEquals(len(json_response),2)

        self.assertEquals(json_response[0]['name'],"bobbybc")
        self.assertEquals(json_response[0]['phone_number'],"9170002894")

        self.assertEquals(json_response[1]['name'],"bill")
        self.assertEquals(json_response[1]['phone_number'],"12312312")

# Test that the customer endpoints are not accessible to an unauthorised user.
    def test_unauthorised_user(self):
        #setup org
        organisation = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisation.code, None, is_staff=True)
        #first, test creating customer
        response = self.client.post(
            '/api/customer/', {'name': 'ralph', 'phone_number': '9170002894'})
        self.assertEquals(response.status_code, 401)

        #secondly, test deleting customer
        delete_response = self.client.delete(f'/api/customer/0/')
        self.assertEquals(delete_response.status_code, 401)

        #thirdly, test partial updating customer
        patch_response = self.client.patch('/api/customer/0/', {'phone_number': "12312332"})
        self.assertEquals(patch_response.status_code, 401)

        #fourthly, test updating customer
        put_response = self.client.patch('/api/customer/0/', { 'name': 'xyz', 'phone_number': "12312368"})
        self.assertEquals(put_response.status_code, 401)

        #lastly, test listing customer
        get_response = self.client.get('/api/customer/')
        self.assertEquals(get_response.status_code,401)

    #Tests the field limits in AreaCode model
    def test_field_validation(self):
        organisation = Organisation.objects.get(name="Farmone")
        user = get_user_model().objects.create_user("email@gmail.com", "first_name",
                                                    "last_name", organisation.code, None, is_staff=True)
        self.client.force_authenticate(user)

        #first test within limits
        response = self.client.post(
            '/api/customer/', {'name': 'a'*50, 'phone_number': "a"*10})
        self.assertEquals(response.status_code, 200)

        #exceed name limit
        response = self.client.post(
            '/api/customer/', {'name': 'a'*51, 'phone_number': "a"*10})
        self.assertEquals(response.status_code, 400)

        #exceed number limit
        response = self.client.post(
            '/api/customer/', {'name': 'a'*50, 'phone_number': "a"*11})
        self.assertEquals(response.status_code, 400)