from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from .models import CustomUser


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'photo', 'about', 'skills')
        read_only_fields = ('email', 'username')


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        # Additional validation for first_name and last_name
        if not data.get('first_name'):
            raise serializers.ValidationError({"first_name": "First name is required."})
        if not data.get('last_name'):
            raise serializers.ValidationError({"last_name": "Last name is required."})

        return super().validate(data)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        return user
