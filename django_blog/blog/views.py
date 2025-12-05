# File: blog/views.py (COMPLETE - No changes required)

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import CustomUserCreationForm, PostForm 
from .models import Post 


# --- Q1: Authentication Views (MUST BE PRESENT) ---

def register(request):
    """Handles user registration using CustomUserCreationForm."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'blog/register.html', context)


@login_required 
def profile(request):
    """Allows authenticated users to view and update their email."""
    user = request.user
    
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email and new_email != user.email:
            user.email = new_email
            user.save()
            messages.success(request, 'Your profile details have been updated!')
            return redirect('profile') 
    
    context = {'user': user}
    return render(request, 'blog/profile.html', context)


# --- Q2: CRUD Class-Based Views ---

# 1. READ (List): Displays all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html' 
    context_object_name = 'posts'
    ordering = ['-published_date'] 

# 2. READ (Detail): Displays a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# 3. CREATE: Allows authenticated users to create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list') 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# 4. UPDATE: Allows the post author to edit their post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# 5. DELETE: Allows the post author to delete their post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list') 

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# --- Q0/Q1: Home redirect function (Must be present) ---

def home_redirect(request):
    """Redirects the root path to the post list view."""
    return redirect('post_list')