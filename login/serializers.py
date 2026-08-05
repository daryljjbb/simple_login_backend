from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile, Note, Task, ActivityLog


# ---------------------------------------------------------
# USER SERIALIZER (includes role)
# ---------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


# ---------------------------------------------------------
# JWT TOKEN SERIALIZER (adds role + username to token)
# Bulletproof: auto‑creates missing UserProfile
# ---------------------------------------------------------

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Ensure profile exists (fixes 500 login crash)
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={"role": "user"}
        )

        # Custom claims
        token["username"] = user.username
        token["role"] = profile.role

        return token

    def validate(self, attrs):
        """
        Override validate() so the response includes:
        - access token
        - refresh token
        - role
        - username
        """
        data = super().validate(attrs)

        # Ensure profile exists again (double safety)
        profile, created = UserProfile.objects.get_or_create(
            user=self.user,
            defaults={"role": "user"}
        )

        data["username"] = self.user.username
        data["role"] = profile.role

        return data


# ---------------------------------------------------------
# NOTE SERIALIZER
# ---------------------------------------------------------

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "category", "created_at"]


# ---------------------------------------------------------
# TASK SERIALIZER
# ---------------------------------------------------------

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "completed", "due_date", "priority", "created_at"]


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = "__all__"
