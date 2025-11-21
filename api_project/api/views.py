from django.shortcuts import render
from django.http import HttpResponse

# Simple view for the project root to confirm the server is running
def api_root(request):
    return HttpResponse("<h1>API Project Setup Successful!</h1><p>Navigate to /admin/ or /api/ for development.</p>")