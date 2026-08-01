from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.decorators import api_view, permission_classes

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, Note, Task
from .serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer,
    NoteSerializer,
    TaskSerializer,
)

# ---------------------------------------------------------
# JWT LOGIN (with role included)
# ---------------------------------------------------------

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, role="user")

        return Response({"message": "User registered successfully."},
                        status=status.HTTP_201_CREATED)


# ---------------------------------------------------------
# PROFILE
# ---------------------------------------------------------

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        user.email = request.data.get("email", user.email)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


# ---------------------------------------------------------
# CHANGE PASSWORD
# ---------------------------------------------------------

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not request.user.check_password(old_password):
            return Response({"error": "Current password is incorrect."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()
        return Response({"message": "Password changed successfully."})


# ---------------------------------------------------------
# ROLE PERMISSIONS
# ---------------------------------------------------------

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "profile") and request.user.profile.role == "admin"

# ---------------------------------------------------------
# ADMIN ROLE MANAGEMENT
# ---------------------------------------------------------

class AdminUserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all().order_by("username")
        data = []

        for user in users:
            data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.profile.role,
                "date_joined": user.date_joined,
            })

        return Response(data)


class AdminUserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.profile.role,
            "date_joined": user.date_joined,
        })


class AdminUpdateRoleView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        new_role = request.data.get("role")

        if new_role not in dict(UserProfile.ROLE_CHOICES):
            return Response({"error": "Invalid role"}, status=400)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.profile.role = new_role
        user.profile.save()

        return Response({"message": f"Role updated to {new_role}"})


class AdminDeleteUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.delete()
        return Response({"message": "User deleted successfully"})

# ---------------------------------------------------------
# ADMIN DASHBOARD EXAMPLE
# ---------------------------------------------------------

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Admin dashboard data"})


# ---------------------------------------------------------
# NOTES
# ---------------------------------------------------------

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def notes_list_create_view(request):
    if request.method == "GET":
        notes = Note.objects.filter(user=request.user).order_by("-created_at")
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def note_detail_view(request, pk):
    try:
        note = Note.objects.get(pk=pk, user=request.user)
    except Note.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == "PUT":
        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        note.delete()
        return Response(status=204)


# ---------------------------------------------------------
# TASKS
# ---------------------------------------------------------

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def tasks_list_create_view(request):
    if request.method == "GET":
        tasks = Task.objects.filter(user=request.user).order_by("completed", "due_date")
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def task_detail_view(request, pk):
    try:
        task = Task.objects.get(pk=pk, user=request.user)
    except Task.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        task.delete()
        return Response(status=204)
