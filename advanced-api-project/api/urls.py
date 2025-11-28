from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookListCreateAPIView, BookDetailAPIView 

# Setup router for ViewSets
router = DefaultRouter()
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    # Router URLs (for authors)
    path('', include(router.urls)), 
    
    # Books - Combined List and Create
    path('books/', BookListCreateAPIView.as_view(), name='book-list'), 
    
    # Books - Detail, Update, Destroy
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
]