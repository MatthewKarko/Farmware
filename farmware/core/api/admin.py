from django.contrib import admin
from .models.organisation import  Organisation
from .models.team import Team

# Register your models here.
admin.site.register(Organisation)
admin.site.register(Team)