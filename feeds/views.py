from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Feed
from .permissions import IsOwnerOrReadOnly
from .serializers import FeedSerializer


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.select_related('user').prefetch_related('user__skills').all()
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
