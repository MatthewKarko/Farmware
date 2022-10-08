from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from ..serialisers import UserSerialiser

class CurrentUserView(APIView):

    def get(self, request):
        serializer = UserSerialiser(request.user)
        return Response(serializer.data)