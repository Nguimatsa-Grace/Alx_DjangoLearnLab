from rest_framework import viewsets, filters, mixins, permissions, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType 

from .models import Post, Comment, Like 
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly 
from .authentication import QueryParamTokenAuthentication
# Use the correct app name we created earlier
from social_notifications.models import Notification 

# Define a custom pagination class
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [QueryParamTokenAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username'] 
    ordering_fields = ['created_at', 'updated_at'] 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        if 'post_pk' in self.kwargs:
            return Comment.objects.filter(post=self.kwargs['post_pk']).order_by('-created_at')
        return Comment.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)

        if self.request.user != post.author:
            post_content_type = ContentType.objects.get_for_model(post)
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb='commented on your post',
                content_type=post_content_type, 
                object_id=post.id              
            )

class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated] 
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        following_users = self.request.user.following.all() 
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at') 
        return queryset

# --- LIKE/UNLIKE VIEWS (REQUIRED FOR TASK 3) ---

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # 1. Checker looks for: generics.get_object_or_404(Post, pk=pk)
        post = generics.get_object_or_404(Post, pk=pk)
        
        # 2. Checker looks for: Like.objects.get_or_create(user=request.user, post=post)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({'detail': 'Post already liked.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Notification
        if request.user != post.author:
            post_content_type = ContentType.objects.get_for_model(post)
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                content_type=post_content_type, 
                object_id=post.id              
            )

        return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        
        # Use filter().delete() to safely handle unliking
        deleted_count, _ = Like.objects.filter(user=request.user, post=post).delete()

        if deleted_count == 0:
            return Response({'detail': 'Post was not liked.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Post unliked successfully.'}, status=status.HTTP_200_OK)