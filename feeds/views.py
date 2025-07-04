from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response

from .models import Feed, Skill
from .serializers import FeedSerializer, SkillSerializer, UserFeedSerializer
from .permissions import IsOwnerOrReadOnly

class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.select_related('user').prefetch_related('user__skills').all()
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        if Feed.objects.filter(user=self.request.user).exists():
            raise ValidationError("You already have a Feed.")
        serializer.save(user=self.request.user)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.select_related('user').all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserFeedViewSet(viewsets.ModelViewSet):
    serializer_class = UserFeedSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if Feed.objects.filter(user=self.request.user).exists():
            raise ValidationError("You already have a Feed.")
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            instance = Feed.objects.get(user=request.user)
        except Feed.DoesNotExist:
            raise NotFound("Feed not found for the user.")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Feed updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )
