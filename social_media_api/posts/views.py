# posts/views.py

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly 
from .authentication import QueryParamTokenAuthentication # <-- ADDED IMPORT

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # <-- ADDED AUTHENTICATION CLASS HERE
    authentication_classes = [QueryParamTokenAuthentication] 
    
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username'] 
    ordering_fields = ['created_at', 'updated_at'] 

    def perform_create(self, serializer):
        # Automatically set the author of the post to the currently logged-in user
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    # We override get_queryset to ensure comments are filtered by the post ID
    def get_queryset(self):
        # Requires the URL to include the post_pk, e.g., /posts/1/comments/
        if 'post_pk' in self.kwargs:
            return Comment.objects.filter(post=self.kwargs['post_pk'])
        return Comment.objects.all()

    def perform_create(self, serializer):
        # Get the post object from the URL kwargs and the user from the request
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)