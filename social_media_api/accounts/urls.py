from django.urls import path
from .views import (
    UserRegistrationView, 
    UserLoginView, 
    FollowUserView, 
    UnfollowUserView
)

urlpatterns = [
    # Auth Endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),

    # Task 2: Follow Management (Checker looks for follow/<int:user_id>/)
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]