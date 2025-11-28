from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Author, Book
from django.urls import reverse

class AuthorAPITestCase(APITestCase):
    """
    Tests for the AuthorViewSet. Ensures basic CRUD operations and permissions.
    """
    def setUp(self):
        # Setup a staff user (for write permissions) and a regular author object
        self.staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        self.author = Author.objects.create(name="H. G. Wells", birth_year=1866)
        
        self.list_url = reverse('author-list') 
        self.detail_url = reverse('author-detail', args=[self.author.id]) 

    def test_author_list_read_only(self):
        """Ensure unauthenticated users can view the list of authors (GET 200)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_create_authenticated(self):
        """Ensure only staff users can create an author (POST 201)."""
        self.client.force_authenticate(user=self.staff_user)
        data = {'name': 'Jules Verne', 'birth_year': 1828}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_author_delete_unauthenticated_fails(self):
        """Ensure unauthenticated users cannot delete an author (DELETE 403)."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookAPITestCase(APITestCase):
    """
    Comprehensive unit tests for the Book API views, covering CRUD, 
    permissions, filtering, searching, and ordering.
    """
    def setUp(self):
        # 1. Create Users for Permission Testing
        self.staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        self.regular_user = User.objects.create_user(username='regularuser', password='password123')

        # 2. Create Authors
        self.author_a = Author.objects.create(name="Isaac Asimov", birth_year=1920)
        self.author_b = Author.objects.create(name="Ursula K. Le Guin", birth_year=1929)
        
        # 3. Create Books
        self.book1 = Book.objects.create(
            title="Foundation", 
            author=self.author_a, 
            publication_year=1951,
            isbn="978-0553293357"
        )
        self.book2 = Book.objects.create(
            title="The Caves of Steel", 
            author=self.author_a, 
            publication_year=1954,
            isbn="978-0586016335"
        )
        self.book3 = Book.objects.create(
            title="The Left Hand of Darkness", 
            author=self.author_b, 
            publication_year=1969,
            isbn="978-0007135017"
        )

        # URLs: book-list is now used for both List (GET) and Create (POST)
        self.list_create_url = reverse('book-list')
        self.detail_url = reverse('book-detail', args=[self.book1.id])
        self.update_url = self.detail_url 
        self.delete_url = self.detail_url 


    # --- 1. CRUD Tests (Staff User) ---

    def test_create_book_authenticated(self):
        """Ensure a staff user can create a new book (POST 201) via the list endpoint."""
        self.client.force_authenticate(user=self.staff_user)
        data = {
            'title': 'The Robots of Dawn',
            'author': self.author_a.id,
            'publication_year': 1983,
            'isbn': '978-0345300344'
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book_authenticated(self):
        """Ensure a staff user can update an existing book (PUT 200)."""
        self.client.force_authenticate(user=self.staff_user)
        updated_title = 'Foundation Updated'
        updated_data = {
            'title': updated_title,
            'author': self.author_a.id,
            'publication_year': 2000, 
            'isbn': self.book1.isbn
        }
        response = self.client.put(self.update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, updated_title)

    def test_delete_book_authenticated(self):
        """Ensure a staff user can delete a book (DELETE 204)."""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2) 


    # --- 2. Permission Tests (Unauthenticated/Regular User) ---

    def test_create_book_unauthenticated_fails(self):
        """Ensure unauthenticated users are blocked from creation (POST 403)."""
        data = {
            'title': 'Test Book', 
            'author': self.author_a.id, 
            'publication_year': 2025
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
        
    def test_update_book_regular_user_fails(self):
        """Ensure non-staff users are blocked from updates (PUT 403)."""
        self.client.force_authenticate(user=self.regular_user)
        updated_data = {
            'title': 'Foundation Updated',
            'author': self.author_a.id,
            'publication_year': 2000, 
            'isbn': self.book1.isbn
        }
        response = self.client.put(self.update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_book_unauthenticated_fails(self):
        """Ensure unauthenticated users are blocked from deletion (DELETE 403)."""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # --- 3. Filtering, Searching, and Ordering Tests ---

    def test_filtering_by_publication_year(self):
        """Ensure filtering by publication_year works correctly."""
        response = self.client.get(self.list_create_url, {'publication_year': 1954})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_searching_by_title_keyword(self):
        """Ensure searching by keyword in the title works correctly."""
        response = self.client.get(self.list_create_url, {'search': 'Darkness'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_ordering_by_title_descending(self):
        """Ensure ordering by title in descending order works correctly."""
        response = self.client.get(self.list_create_url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "The Left Hand of Darkness")