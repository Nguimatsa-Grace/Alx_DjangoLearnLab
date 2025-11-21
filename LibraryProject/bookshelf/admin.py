from django.contrib import admin
from .models import Book # <-- ONLY importing Book here

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'is_available', 'date_added')
    list_filter = ('is_available', 'author')
    search_fields = ('title', 'author', 'isbn')
    ordering = ('title',)