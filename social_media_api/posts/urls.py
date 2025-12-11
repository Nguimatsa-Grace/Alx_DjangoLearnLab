# posts/urls.py

from django.urls import path, include
from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet # This import must match the class names in views.py

# Main router for posts
router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)

# Nested router for comments (under posts)
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    # Includes /posts/ routes
    path('', include(router.urls)),
    # Includes /posts/{post_pk}/comments/ routes
    path('', include(posts_router.urls)),
]