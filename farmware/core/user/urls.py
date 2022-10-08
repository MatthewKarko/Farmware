from django.urls import path

from rest_framework.routers import DefaultRouter

from .views.BlacklistTokenUpdateView import BlacklistTokenUpdateView
from .views.CurrentUserView import CurrentUserView
from .views.UserRegistrationView import UserRegistrationView
from .viewsets import UserViewSet


router = DefaultRouter()
app_name = 'user'

router.register('', UserViewSet, 'user')

urlpatterns = [
    # Register user endpoint
    path('register/', UserRegistrationView.as_view(), name="register_user"),

    # JWT token blacklist
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),

    # Sanity check
    path('me/', CurrentUserView.as_view(), name='me'),
]

urlpatterns += router.urls