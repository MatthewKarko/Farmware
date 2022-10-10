from django.conf.urls import url
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views.ActivateAccount import ActivateAccount
from .views.BlacklistTokenUpdateView import BlacklistTokenUpdateView
from .views.CurrentUserView import CurrentUserView
from .views.UserRegistrationView import UserRegistrationView
from .viewsets import UserViewSet


router = DefaultRouter()
app_name = 'user'

router.register('', UserViewSet, 'user')

urlpatterns = [
    # Register user endpoint
    # path('register/', UserRegistrationView.as_view(), name="register_user"),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     activate, name='activate'),
    path('activate/<uidb64>/<token>', ActivateAccount.as_view(), name='activate'),

    # JWT token blacklist
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),

    # Sanity check
    path('me/', CurrentUserView.as_view(), name='me'),
]

urlpatterns += router.urls