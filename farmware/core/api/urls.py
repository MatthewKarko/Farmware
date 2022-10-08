<<<<<<< HEAD
from django.urls import path

from .views import OrganisationsView, UsersView

urlpatterns = [
    path('', OrganisationsView.as_view(), name='NAME NAME TEST'),
]
=======
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import OrganisationsView
from .viewsets import TeamViewSet

router = DefaultRouter()

router.register('teams', TeamViewSet, 'team')

urlpatterns = [
    path('', OrganisationsView.as_view(), name='NAME NAME TEST'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
>>>>>>> master
