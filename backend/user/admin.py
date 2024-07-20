"""
User admin 
"""
from user.models import *
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
        model = CustomUser
        ordering = ('id',)
        list_filter = ('id',)
        list_display = ('id',)
        search_fields = ('id',)
        fieldsets = (
        (None, {'fields': ('id', 'name', 'is_superuser', 'is_admin', 'is_staff')}),
        )
        add_fieldsets = (
                (None, {'fields':  ('id', 'name', 'is_superuser', 'is_admin', 'is_staff')}),
        )