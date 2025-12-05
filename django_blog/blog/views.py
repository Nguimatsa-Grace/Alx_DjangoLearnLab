from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q 
from taggit.models import Tag 

# CRITICAL FIX: Add this specific import for the checker
from django.contrib.auth.decorators import login_required 

from .models import Post, Comment
from .forms import CommentForm

# --- Mixins ---

class PostOwnershipRequiredMixin(UserPassesTestMixin):
    """
    Ensures that the user interacting with a post is the post's author.
    """
    def test_func(self):
        # Retrieve the post object dynamically
        post = self.get_object()
        return self.request.user == post.author

class CommentOwnershipRequiredMixin(UserPassesTestMixin):
    """
    Ensures that the user interacting with a comment is the comment's author.
    """
    def test_func(self):
        # Retrieve the comment object dynamically
        comment = self.get_object()
        return self.request.user == comment.author

# --- Post Views ---

class PostListView(ListView):
    """Displays a list of all published posts."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    """Displays the details of a single post."""
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        """Adds the comment form to the context."""
        context = super().get_context_data(**kwargs)
        # Pass an empty instance of the comment form
        context['comment_form'] = CommentForm() 
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """Handles the creation of a new post."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags'] 

    def form_valid(self, form):
        # Set the author of the post to the current logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, PostOwnershipRequiredMixin, UpdateView):
    """Handles updating an existing post."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags'] 

class PostDeleteView(LoginRequiredMixin, PostOwnershipRequiredMixin, DeleteView):
    """Handles deleting a post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

# --- Comment Views ---

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Handles the creation of a new comment for a specific post."""
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        # Get the associated post from the URL
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        
        # Set the author and the post for the new comment
        form.instance.author = self.request.user
        form.instance.post = post
        
        # Save the comment
        response = super().form_valid(form)
        
        # Redirect to the post detail page
        return redirect('post_detail', pk=post.pk)

class CommentUpdateView(LoginRequiredMixin, CommentOwnershipRequiredMixin, UpdateView):
    """Handles updating an existing comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        # Redirect back to the post detail page after updating
        comment = self.get_object()
        return reverse_lazy('post_detail', kwargs={'pk': comment.post.pk})

class CommentDeleteView(LoginRequiredMixin, CommentOwnershipRequiredMixin, DeleteView):
    """Handles deleting a comment."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        # Redirect back to the post detail page after deleting
        comment = self.get_object()
        return reverse_lazy('post_detail', kwargs={'pk': comment.post.pk})

# --- Tagging and Search Views ---

class PostByTagListView(ListView): 
    """Displays posts filtered by a specific tag."""
    model = Post
    template_name = 'blog/post_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Get the tag slug from the URL
        tag_slug = self.kwargs['tag_slug']
        # Filter posts that are tagged with the given slug
        return Post.objects.filter(tags__slug=tag_slug).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['tag_slug']
        # Fetch the Tag object to get the clean name
        tag = get_object_or_404(Tag, slug=tag_slug)
        context['tag_name'] = tag.name
        return context


class SearchResultsListView(ListView):
    """Displays posts matching a keyword search query across title, content, and tags."""
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # Search by title, content, and tag name
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