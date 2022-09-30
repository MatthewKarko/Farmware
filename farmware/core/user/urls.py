from django.urls import path
from .views import UserRegistration #, BlacklistTokenUpdateView

app_name = 'user'

urlpatterns = [
    # Register user endpoint
    path('register/', UserRegistration.as_view(), name="register_user"),

    # TODO: leave for now; 
    # path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
    #      name='blacklist')
]