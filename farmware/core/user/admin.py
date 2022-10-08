from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import TextInput, Textarea, CharField

from .models import User


class UserAdminConfig(UserAdmin):
    model = User
    readonly_fields = ('id',)
    search_fields = ('email', 'first_name', 'organisation')
    list_filter = ('email', 'first_name', 'organisation', 'is_active', 'is_staff')
    ordering = ('first_name',)
    list_display = ('email', 'first_name','organisation',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('id','email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Organisation', {'fields': ('organisation','role', 'teams')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'organisation', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(User, UserAdminConfig)