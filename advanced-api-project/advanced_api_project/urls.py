from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

# Set up the router for ViewSets
# 
router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet)
router.register(r'books', views.BookViewSet)

urlpatterns = [
    # Django Admin site
    path('admin/', admin.site.urls),
    
    # API endpoints for authors and books
    # The 'router.urls' creates /api/authors/ and /api/books/
    path('api/', include(router.urls)),
]