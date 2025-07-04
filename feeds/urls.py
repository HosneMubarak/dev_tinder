from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'feeds', FeedViewSet, basename='feed')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'user-feed', UserFeedViewSet, basename='user-feed')
router.register(r'connections', ConnectionRequestViewSet, basename='connections')

urlpatterns = [
    path('', include(router.urls)),
]
