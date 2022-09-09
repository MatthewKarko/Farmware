from django.contrib.auth import authenticate, login

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .serialisers import TeamSerialiser


class TeamViewSet(ModelViewSet):
    """Team View"""

    serializer_class = TeamSerialiser
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        # if not self.request.session.exists(self.request.session.session_key):
        #     self.request.session.create()
        data = request.data

        print('session:', request.user)

        print(data)

        # Ensure data is valid
        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exception=True)

        team = serialiser.save()

        return Response({'success': 'Team created'}, status=status.HTTP_200_OK)