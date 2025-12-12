from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, PostFeedView, LikePostView, UnlikePostView

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    # Task 2: Feed route
    path('feed/', PostFeedView.as_view(), name='post-feed'),
    
    # Task 3: Like/Unlike routes
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    
    # Include router URLs
    path('', include(router.urls)),
]