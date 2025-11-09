from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm # ✅ New Import
from django.urls import reverse_lazy                   # ✅ New Import
from django.views.generic import CreateView            # ✅ New Import

# Create your views here.

# 👇 ADD THIS CLASS DEFINITION
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# Create your views here.
