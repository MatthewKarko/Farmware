from django.conf.urls import url
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views.ActivateAccount import ActivateAccount
from .views.BlacklistTokenUpdateView import BlacklistTokenUpdateView
from .views.CurrentUserView import CurrentUserView
from .viewsets import UserViewSet


router = DefaultRouter()
app_name = 'user'

router.register('', UserViewSet,'user')

urlpatterns = [
    # Activate account
    path('activate/<uidb64>/<token>', ActivateAccount.as_view(), name='activate'),

    # JWT token blacklist
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    # Sanity check
    path('me/', CurrentUserView.as_view(), name='me'),
]

urlpatterns += router.urls
