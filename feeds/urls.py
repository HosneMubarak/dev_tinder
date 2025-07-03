# feeds/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FeedViewSet

router = DefaultRouter()
router.register(r'feeds', FeedViewSet, basename='feed')

urlpatterns = [
    path('', include(router.urls)),
]
