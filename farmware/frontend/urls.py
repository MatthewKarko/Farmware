from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from .views import index

urlpatterns = [
    path('', index),
    path('login', index),
    path('signup', index),
    path('logout', index),
    path('dashboard',index),
    path('accountsettings',index),
    path('userstable',index),
    path('order',index),
    path('produce',index),
    path('customers',index),
    path('suppliers',index),
    path('teams',index),
    path('docs/',include_docs_urls(title='FarmwareAPI')),
    path('schema', get_schema_view(
        title='FarmwareAPI',
        description='API for FarmwareAPI',
        version="1.0.0"
    ),name='openapi-schema'),
]