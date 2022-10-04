from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

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
            user = serializer.save()
            if user:
                refresh = RefreshToken.for_user(user)

                response = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serializer.data,
                }
                return Response(response, status=status.HTTP_201_CREATED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)