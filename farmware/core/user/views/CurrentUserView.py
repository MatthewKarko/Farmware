from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import User
from ..serialisers import UserSerialiser

class CurrentUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerialiser(request.user)
        return Response(serializer.data)