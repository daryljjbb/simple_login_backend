from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile, Note, Task


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
# ---------------------------------------------------------

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims
        token["username"] = user.username
        token["role"] = getattr(user.profile, "role", "user")

        return token


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
