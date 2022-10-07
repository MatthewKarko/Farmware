from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ..models import User
from ..serialisers import RegisterUserSerialiser, RegisterAdminSerialiser

TRUE = 'TRUE'
FALSE = 'FALSE'


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        # See if a new organisation is trying to be made
        if data.get('new_org', FALSE).upper() == TRUE:
            serializer = RegisterAdminSerialiser(data=data)
        else:
            serializer = RegisterUserSerialiser(data=data)

        if serializer.is_valid():
            user: User = serializer.save()
            if user:
                # TODO: send confirmation email
                return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)