# posts/views.py (INCLUDING FeedViewSet)

from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly 
from .authentication import QueryParamTokenAuthentication

# Define a custom pagination class (required for Step 5 of the previous task)
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [QueryParamTokenAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination # Applying pagination
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
            return Comment.objects.filter(post=self.kwargs['post_pk'])
        return Comment.objects.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)

# --- NEW FEED VIEWSET ---
class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Returns a list of posts from all users that the current authenticated user is following.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        # 1. Get the list of users the current user is following
        followed_users = self.request.user.following.all()

        # 2. Filter posts to only include those from followed users
        #    and exclude the current user's own posts (optional, but standard for a feed)
        queryset = Post.objects.filter(
            author__in=followed_users
        ).order_by('-created_at') # Order by newest first

        return queryset