from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status, generics, permissions
from .models import CustomUser
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Post
from .serializers import PostSerializer
from rest_framework.exceptions import NotFound
'''
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({'token': str(token)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def follow_user(request, user_id):
    target_user = User.objects.get(id=user_id)
    request.user.following.add(target_user)
    return Response({"message": f"You are now following {target_user.username}."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def unfollow_user(request, user_id):
    target_user = User.objects.get(id=user_id)
    request.user.following.remove(target_user)
    return Response({"message": f"You have unfollowed {target_user.username}."}, status=status.HTTP_200_OK)
'''

User = get_user_model()

class FollowUserView(generics.GenericAPIView):
    queryset = User.objects.all()  # Ensure CustomUser.objects.all() is here
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            target_user = self.get_queryset().get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found.")

        request.user.following.add(target_user)
        return Response({"message": f"You are now following {target_user.username}."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    