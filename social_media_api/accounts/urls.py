from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView

urlpatterns = [
    # Required for Task 0 and Task 1:
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]