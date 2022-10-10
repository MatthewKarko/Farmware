from django.contrib import admin
from django.urls import include, path
# from allauth.account.views import confirm_email

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # API
    path('api/', include(('core.api.urls', 'core'), namespace='api')),
    
    # REST Framework API-Auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', include('frontend.urls')),

    # TODO: leave for now; rest-auth urls
    # url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    # url(r'^account/', include('allauth.urls')),
    # url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
]
