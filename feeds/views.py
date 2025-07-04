from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .serializers import *


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


class ConnectionRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ConnectionRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Return all requests where user is either sender or receiver
        return ConnectionRequest.objects.filter(
            models.Q(from_user=user) | models.Q(to_user=user)
        ).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    @action(detail=False, methods=['get'])
    def sent(self, request):
        """List sent requests by current user"""
        qs = ConnectionRequest.objects.filter(from_user=request.user).order_by('-created')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def received(self, request):
        """List received requests by current user (pending only)"""
        qs = ConnectionRequest.objects.filter(to_user=request.user, status='pending').order_by('-created')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """Accept or decline a received connection request"""
        try:
            conn_req = ConnectionRequest.objects.get(pk=pk, to_user=request.user, status='pending')
        except ConnectionRequest.DoesNotExist:
            raise NotFound("Connection request not found or already responded.")

        action = request.data.get('action')
        if action not in ['accept', 'decline']:
            return Response({"detail": "Invalid action. Use 'accept' or 'decline'."},
                            status=status.HTTP_400_BAD_REQUEST)

        conn_req.status = 'accepted' if action == 'accept' else 'declined'
        conn_req.save()
        serializer = self.get_serializer(conn_req)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path="my-connections")
    def connections(self, request):
        """List all accepted connections of the current user"""
        user = request.user
        qs = ConnectionRequest.objects.filter(
            status='accepted'
        ).filter(
            models.Q(from_user=user) | models.Q(to_user=user)
        ).order_by('-created')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
