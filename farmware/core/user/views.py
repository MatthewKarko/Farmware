import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .models import User
from .serialisers import RegisterUserSerialiser, RegisterAdminSerialiser


class UserRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        # See if a new organisation is trying to be made
        if data.get('new_org', False) == 'True':
            serializer = RegisterAdminSerialiser(data=data)
        else:
            serializer = RegisterUserSerialiser(data=data)

        if serializer.is_valid():
            user: User = serializer.save()
            if user:
                # TODO: send confirmation email
                return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)