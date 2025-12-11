# posts/urls.py (INCLUDING FeedViewSet ROUTE)

from django.urls import path, include
from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet, FeedViewSet # <-- ADDED FeedViewSet

# Main router for posts
router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)

# Register the FeedViewSet to create the /feed/ endpoint
# We use base_name='feed' and an empty prefix '' to put it at the root of the posts app's include.
router.register(r'feed', FeedViewSet, basename='feed') 

# Nested router for comments (under posts)
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    # Includes /posts/ routes AND /feed/ route
    path('', include(router.urls)),
    # Includes /posts/{post_pk}/comments/ routes
    path('', include(posts_router.urls)),
]