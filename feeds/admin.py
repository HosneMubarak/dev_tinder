from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ["user", "about"]
