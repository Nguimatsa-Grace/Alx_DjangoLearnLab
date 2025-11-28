from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

# Set up the router for ViewSets (Only for the Author model now)
router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet)

urlpatterns = [
    # 1. Django Admin site
    path('admin/', admin.site.urls),
    
    # 2. API Endpoints (Using the router for the Author model)
    path('api/', include(router.urls)),
    
    # 3. Explicit Generic View Endpoints for the Book Model (Step 2)
    # List (GET) and Create (POST)
    path('api/books/', views.BookList.as_view(), name='book-list'),
    path('api/books/create/', views.BookCreate.as_view(), name='book-create'),
    
    # Detail (GET), Update (PUT/PATCH), and Delete (DELETE)
    path('api/books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('api/books/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('api/books/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    
    # Required for testing permissions in the browsable API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]