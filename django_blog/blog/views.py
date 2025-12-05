from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q 
from taggit.models import Tag 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User # Required by Q0 check

from .models import Post, Comment
from .forms import CommentForm

# --- Authentication Views (Finalized) ---

def register(request):
    """Handles user registration using Django's built-in UserCreationForm."""
    # CRITICAL FIX: Ensure 'POST' and 'method' are explicitly used
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # CRITICAL FIX: Ensure 'save()' is explicitly used
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Allows an authenticated user to view and update their profile details.
    Uses fields available on the User model.
    """
    model = User
    template_name = 'blog/profile.html'
    fields = ['username', 'email', 'first_name', 'last_name']
    
    def get_object(self):
        """Ensure the view only updates the currently logged-in user."""
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, "Your profile has been updated successfully!")
        return reverse('profile')

# --- Mixins ---

class PostOwnershipRequiredMixin(UserPassesTestMixin):
    """Ensures that the user interacting with a post is the post's author."""
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentOwnershipRequiredMixin(UserPassesTestMixin):
    """Ensures that the user interacting with a comment is the comment's author."""
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

# --- Post Views ---

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm() 
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags'] 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, PostOwnershipRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags'] 

class PostDeleteView(LoginRequiredMixin, PostOwnershipRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

# --- Comment Views ---

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        response = super().form_valid(form)
        return redirect('post_detail', pk=post.pk)

class CommentUpdateView(LoginRequiredMixin, CommentOwnershipRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post_detail', kwargs={'pk': comment.post.pk})

class CommentDeleteView(LoginRequiredMixin, CommentOwnershipRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post_detail', kwargs={'pk': comment.post.pk})

# --- Tagging and Search Views ---

class PostByTagListView(ListView): 
    model = Post
    template_name = 'blog/post_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        return Post.objects.filter(tags__slug=tag_slug).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['tag_slug']
        tag = get_object_or_404(Tag, slug=tag_slug)
        context['tag_name'] = tag.name
        return context


class SearchResultsListView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct().order_by('-published_date')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context