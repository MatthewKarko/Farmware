from django.urls import path

from .views import OrganisationsView, UsersView

urlpatterns = [
    path('', OrganisationsView.as_view(), name='NAME NAME TEST'),
]
