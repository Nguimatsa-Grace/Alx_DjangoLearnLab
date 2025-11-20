from django.urls import path
from . import views

urlpatterns = [
    # General views
    path('books/', views.book_list, name='book_list'),
    path('search/', views.book_search_secure, name='book_search_secure'), # New Secure Search URL
    path('secure-csp/', views.secure_csp_view, name='secure_csp_view'), # New CSP URL
    path('submit-form/', views.submit_book_form, name='submit_book_form'), # Form Submission Handler
    
    # Custom permission views
    path('create/', views.create_book, name='create_book'),
    path('delete/', views.delete_book, name='delete_book'),
]