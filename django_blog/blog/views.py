# File: blog/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Import our new form
from .forms import CustomUserCreationForm 
from django.contrib.auth.models import User

# --- Existing view from Q0 ---
def post_list(request):
    return render(request, 'blog/index.html', {})
# --- End existing view ---


# --- Custom Registration View ---
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: Log the user in immediately after registration
            # login(request, user) 
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login') # Redirect to the login page
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'blog/register.html', context)


# --- Profile Management View ---
@login_required # Ensures only logged-in users can access this page
def profile(request):
    user = request.user
    
    # Simple logic to update basic profile details (email)
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email and new_email != user.email:
            user.email = new_email
            user.save()
            messages.success(request, 'Your profile details have been updated!')
            return redirect('profile') # Redirect to clear the POST data
    
    # For GET request or after POST
    context = {'user': user}
    return render(request, 'blog/profile.html', context)