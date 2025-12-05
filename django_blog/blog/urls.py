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
    PostByTagListView,
    SearchResultsListView, 
)

urlpatterns = [
    # Post URLs
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    
    # CRITICAL FIX for Q2: Must be 'update/' not 'edit/'
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # Comment URLs
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # Tagging and Search URLs
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'), 
    path('search/', SearchResultsListView.as_view(), name='search_results'),          
]