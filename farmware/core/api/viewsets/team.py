from django.db import IntegrityError
from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from ..models.team import Team
from ..serialisers import TeamCreationSerialiser, TeamSerialiser
from ...user.models import User
from ...user.permissions import IsInOrganisation


class TeamViewSet(ModelViewSet):
    """Team View"""
    serializer_class = TeamCreationSerialiser
    permission_classes = [IsAuthenticated, IsInOrganisation]
    # queryset = Team.objects.all()

    def get_queryset(self, **kwargs):
        user: User = self.request.user
        return Team.objects.all().filter(
            organisation=user.organisation,
            **kwargs
            )

    def create(self, request, *args, **kwargs):
        data: QueryDict = request.data

        self.serializer_class = TeamCreationSerialiser
        serialiser = self.get_serializer(data=data)

        # Ensure data is valid
        serialiser.is_valid(raise_exception=True)

        try:
            serialiser.save()
        except IntegrityError:
            return Response({'error': 
            'A team of that category already exists in your organisation.'}, 
            status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Team created.'}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        serialiser = TeamSerialiser(self.get_queryset(), many=True)
        return Response(serialiser.data)