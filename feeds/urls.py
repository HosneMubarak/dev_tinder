from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FeedViewSet, SkillViewSet, UserFeedViewSet

router = DefaultRouter()
router.register(r'feeds', FeedViewSet, basename='feed')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'user-feed', UserFeedViewSet, basename='user-feed')

urlpatterns = [
    path('', include(router.urls)),
]
