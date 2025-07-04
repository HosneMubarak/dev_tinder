from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'last_login',
            'date_joined',
        ]
        read_only_fields = [
            'id',
            'last_login',
            'date_joined',
        ]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']


class FeedSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skills = SkillSerializer(source="user.skills", many=True, read_only=True)

    class Meta:
        model = Feed
        fields = ['user', 'photo', 'about', 'skills']


class UserFeedSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(source="user.skills", many=True, read_only=True)

    class Meta:
        model = Feed
        fields = ['id', 'photo', 'about', 'skills']


class ConnectionRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    to_user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='to_user',
        write_only=True
    )

    class Meta:
        model = ConnectionRequest
        fields = ['id', 'from_user', 'to_user', 'to_user_id', 'status', 'created']
        read_only_fields = ['id', 'from_user', 'to_user', 'status', 'created']

    def validate(self, attrs):
        to_user = attrs['to_user']
        from_user = self.context['request'].user
        if from_user == to_user:
            raise serializers.ValidationError("You cannot send a connection request to yourself.")
        if ConnectionRequest.objects.filter(from_user=from_user, to_user=to_user, status='pending').exists():
            raise serializers.ValidationError("You already have a pending request to this user.")
        return attrs

    def create(self, validated_data):
        from_user = self.context['request'].user
        to_user = validated_data['to_user']
        return ConnectionRequest.objects.create(from_user=from_user, to_user=to_user)
