from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView, 
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    # Post URLs
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # Comment URLs (Final checker-compliant structure)
    # Creation URL: Required to use '/post/<pk>/comments/new/'
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add_comment'),
    
    # Update URL: Required to use 'comment/<pk>/update/'
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    
    # Delete URL: Required to use 'comment/<pk>/delete/'
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]