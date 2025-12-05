# File: myblog/views.py

from django.shortcuts import render

def post_list(request):
    # This will render the index.html template we create next
    return render(request, 'myblog/index.html', {})