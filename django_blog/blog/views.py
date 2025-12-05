from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden

from .models import Post, Comment
from .forms import PostForm, CommentForm

# --- Post Views ---

class PostListView(ListView):
    """Displays a list of all published blog posts."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    """Displays the detail page for a single post."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        """Adds the comment form to the context."""
        context = super().get_context_data(**kwargs)
        # Pass an instance of the CommentForm to the template
        context['comment_form'] = CommentForm() 
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """Allows authenticated users to create a new post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Sets the author to the current logged-in user before saving."""
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows a post author to update their existing post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        """Ensures only the author can edit the post."""
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows a post author to delete their post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        """Ensures only the author can delete the post."""
        post = self.get_object()
        return post.author == self.request.user

# --- Comment Views ---

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Handles creating a new comment on a specific post."""
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        """
        Sets the author and the target post before saving the comment.
        """
        # The URL pattern provides the post's PK as 'pk' in the kwargs
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Redirects back to the detail page of the post."""
        post_pk = self.kwargs['pk']
        return reverse('post_detail', kwargs={'pk': post_pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows a comment author to update their comment."""
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'
    context_object_name = 'comment'

    def get_success_url(self):
        """Redirects back to the detail page of the post the comment belongs to."""
        return self.object.post.get_absolute_url()

    def test_func(self):
        """Ensures only the author can edit the comment."""
        comment = self.get_object()
        return comment.author == self.request.user

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows a comment author to delete their comment."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        """Redirects back to the detail page of the post the comment belonged to."""
        return self.object.post.get_absolute_url()

    def test_func(self):
        """Ensures only the author can delete the comment."""
        comment = self.get_object()
        return comment.author == self.request.user