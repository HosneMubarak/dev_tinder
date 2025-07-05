from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ConnectionRequest, NotInterestedUser
from .serializers import ConnectionRequestSerializer
from users.serializers import CustomUserDetailsSerializer

User = get_user_model()

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

    @action(detail=False, methods=['get'], url_path="accepted-connections")
    def accepted_connections(self, request):
        """List all accepted connections of the current user"""
        user = request.user
        qs = ConnectionRequest.objects.filter(
            status='accepted'
        ).filter(
            models.Q(from_user=user) | models.Q(to_user=user)
        ).order_by('-created')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='explore-users')
    def explore_users(self, request):
        current_user = request.user

        # Get all users that the current user has any connection with
        connected_user_ids = ConnectionRequest.objects.filter(
            models.Q(from_user=current_user) | models.Q(to_user=current_user)
        ).values_list('from_user', 'to_user')

        # Flatten and deduplicate
        user_ids = set()
        for from_id, to_id in connected_user_ids:
            user_ids.add(from_id)
            user_ids.add(to_id)

        # Remove current user's ID
        user_ids.discard(current_user.id)

        # Get not interested users
        not_interested_ids = NotInterestedUser.objects.filter(
            user=current_user
        ).values_list('not_interested_user', flat=True)

        # Exclude connected, not interested, and self
        qs = User.objects.exclude(id__in=user_ids).exclude(id__in=not_interested_ids).exclude(id=current_user.id)

        serializer = CustomUserDetailsSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path="not-interested")
    def mark_not_interested(self, request, pk=None):
        try:
            not_interested_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User not found.")

        if not_interested_user == request.user:
            return Response({"detail": "You cannot mark yourself as not interested."}, status=400)

        obj, created = NotInterestedUser.objects.get_or_create(
            user=request.user,
            not_interested_user=not_interested_user
        )

        return Response({"detail": "User marked as not interested."}, status=200 if created else 204)
