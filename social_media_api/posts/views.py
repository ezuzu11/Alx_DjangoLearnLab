from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from notifications.models import Notification
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']  # Allow searching by title and content

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    def get_queryset(self):
        # Get the current user’s following list
        following_users = self.request.user.following.all()
        # Filter posts by followed users and order by creation date
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

class LikePostView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:  # If the like was created, generate a notification
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )
            return Response({"message": "You liked the post."})
        return Response({"message": "You have already liked this post."}, status=400)

class UnlikePostView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        post = Post.objects.get(id=pk)
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({"message": "You unliked the post."})
    
class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    #serializer_class = NotificationSerializer  # Create this serializer as needed

    def get_queryset(self):
        return self.request.user.notifications.all()
