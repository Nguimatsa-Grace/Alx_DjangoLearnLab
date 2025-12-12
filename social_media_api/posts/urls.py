# posts/urls.py (UPDATED with Like/Unlike Routes)

from django.urls import path, include
from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet, FeedViewSet, LikePostView, UnlikePostView # <-- IMPORTED LIKE VIEWS

# Main router for posts
router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)

# Register the FeedViewSet to create the /feed/ endpoint
router.register(r'feed', FeedViewSet, basename='feed') 

# Nested router for comments (under posts)
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    # Includes /posts/ routes AND /feed/ route
    path('', include(router.urls)),
    # Includes /posts/{post_pk}/comments/ routes
    path('', include(posts_router.urls)),

    # --- NEW ROUTES FOR LIKES ---
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='post-like'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='post-unlike'),
]