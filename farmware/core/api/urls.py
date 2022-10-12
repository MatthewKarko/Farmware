from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import OrganisationsView
from .viewsets import ProduceViewSet
from .viewsets import ProduceVarietyViewSet
from .viewsets import ProduceQuantitySuffixViewSet
from .viewsets import TeamViewSet

router = DefaultRouter()

router.register('produce', ProduceViewSet, 'produce')
router.register('produce_variety', ProduceVarietyViewSet, 'produce_variety')
router.register('produce_quantity_suffix', ProduceQuantitySuffixViewSet, 'produce_quantity_suffix')
router.register('teams', TeamViewSet, 'team')

urlpatterns = [
    # Organisation
    path('organisation/', OrganisationsView.as_view(), name='api-organisation'),

    # User
    ## User
    path('user/', include('core.user.urls', namespace='user')),
    ## Tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns += router.urls
