from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response 

from .models import Organisation
from .serialisers import (
    OrganisationSerialiser
    )

class OrganisationsView(generics.CreateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerialiser


# class CreateUserView(APIView):
#     serliaser_class = CreateUserSerialiser

#     def post(self, request, format=None):
#         if not self.request.session.exists(self.request.session.session_key):
#             self.request.session.create()

#         serliaser = self.serliaser_class(data=request.data)

#         if serliaser.is_valid():
#             first_name = serliaser.data.first_name
#             last_name = serliaser.data.last_name
#             email = serliaser.data.email

#             org_sign_up: bool = serliaser.data.sign_up_as_org

#             # See if an org code came through
#             organisation_code = serliaser.data.get('organisation_code', None)

#             if organisation_code == None: 
#                 # No org code, thus create new org
#                 # org = new org?
#                 # role = admin
#                 # TODO: maybe, the endpoint is wrong? signup-org?
#                 pass
#             else:
#                 # Org code is given, see if it exists
#                 queryset = Organisation.objects.filter(
#                     org_code=organisation_code
#                     )

#                 if queryset.exists():
#                     # Org exists, create a user
#                     org = queryset[0]
#                     print('org:', org)
#                 else:
#                     # Org does not exist, send an error
#                     print('org does not exist')

