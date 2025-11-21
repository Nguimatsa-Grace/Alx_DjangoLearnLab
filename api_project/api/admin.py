from django.contrib import admin
from .models import Book # 🚨 STEP 1: Import the Book model

# STEP 2: Register your models here so they appear in the Django Admin panel
admin.site.register(Book)