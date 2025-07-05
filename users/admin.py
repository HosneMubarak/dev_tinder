from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name','is_staff']
    list_editable = ['first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('photo', 'about', 'skills')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('photo', 'about', 'skills')}),
    )
