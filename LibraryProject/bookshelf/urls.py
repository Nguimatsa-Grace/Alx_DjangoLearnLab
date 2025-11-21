from django.urls import path
from . import views

urlpatterns = [
    # The root URL of the app now maps to the book_list view
    path('', views.book_list, name='dashboard'), 
]