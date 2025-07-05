from django.contrib import admin
from .models import *


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ["from_user", "to_user", "status"]
    list_editable = ["status"]
