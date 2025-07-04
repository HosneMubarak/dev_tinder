from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Feed, Skill


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