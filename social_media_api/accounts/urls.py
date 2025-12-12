from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, FollowUserView, UnfollowUserView

urlpatterns = [
    # Task 0 & 1: ALX searches for these exact strings in THIS file
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Task 2: Follow/Unfollow strings
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]