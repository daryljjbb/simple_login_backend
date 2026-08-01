from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return JsonResponse({'message': 'Login successful', 'user': username})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'POST required'}, status=400)

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=409)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({'message': 'User created successfully', 'user': user.username})

    return JsonResponse({'error': 'POST required'}, status=400)


from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'message': 'Login successful',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': username
        })

    return JsonResponse({'error': 'POST required'}, status=400)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    return Response({"message": f"Welcome {request.user.username}!"})




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user

    return Response({
        "username": user.username,
        "email": user.email,
        "date_joined": user.date_joined,
        "last_login": user.last_login,
    })

