from rest_framework.routers import SimpleRouter

from core.api.viewsets import TeamViewSet
from core.auth.viewsets import LoginViewSet, RegistrationViewSet


routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')

# USER
# routes.register(r'user', UserViewSet, basename='user')

# OTHER
routes.register(r'team', TeamViewSet, basename='team')

urlpatterns = [
    *routes.urls
]