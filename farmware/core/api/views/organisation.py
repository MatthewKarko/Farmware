from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response 

from ..models.organisation import Organisation
from ..serialisers import OrganisationSerialiser

class OrganisationsView(generics.CreateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerialiser