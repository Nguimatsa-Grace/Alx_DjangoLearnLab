from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Author, Book
from django.urls import reverse

class BookAPITestCase(APITestCase):
    """
    Comprehensive unit tests for the Book model's generic API views,
    covering CRUD operations, permission enforcement, filtering, searching, and ordering.
    """
    def setUp(self):
        """
        Set up initial data for testing, including users, authors, and books.
        """
        # 1. Create Users for Permission Testing
        # staff_user is used for authenticated actions (POST, PUT, DELETE)
        self.staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        # regular_user is used for authenticated but non-staff actions (should fail PUT/DELETE)
        self.regular_user = User.objects.create_user(username='regularuser', password='password123')

        # 2. Create Authors
        self.author_a = Author.objects.create(name="Isaac Asimov", birth_year=1920)
        self.author_b = Author.objects.create(name="Ursula K. Le Guin", birth_year=1929)
        
        # 3. Create Books with distinct data for filtering/searching/ordering tests
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

        # URLs for CRUD operations
        # Note: We use the names defined in your advanced_api_project/urls.py
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
        self.detail_url = reverse('book-detail', args=[self.book1.id])
        self.update_url = reverse('book-update-pk', args=[self.book1.id])
        self.delete_url = reverse('book-delete-pk', args=[self.book1.id])


    # --- 1. CRUD Tests for Book Model ---

    def test_list_books(self):
        """Ensure the book list endpoint retrieves all books."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book(self):
        """Ensure retrieving a single book instance is successful."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Foundation')

    def test_create_book_authenticated(self):
        """Ensure a staff user can create a new book (POST)."""
        self.client.force_authenticate(user=self.staff_user)
        data = {
            'title': 'The Robots of Dawn',
            'author': self.author_a.id,
            'publication_year': 1983,
            'isbn': '978-0345300344'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_update_book_authenticated(self):
        """Ensure a staff user can update an existing book (PUT)."""
        self.client.force_authenticate(user=self.staff_user)
        updated_data = {
            'title': 'Foundation Updated',
            'author': self.author_a.id,
            'publication_year': 2000, # Changed year
            'isbn': self.book1.isbn
        }
        response = self.client.put(self.update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.publication_year, 2000)

    def test_delete_book_authenticated(self):
        """Ensure a staff user can delete a book (DELETE)."""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())


    # --- 2. Permission Tests (IsAuthenticatedOrReadOnly) ---

    def test_create_book_unauthenticated_fails(self):
        """Ensure unauthenticated users are blocked from creation."""
        data = {
            'title': 'Test Book', 
            'author': self.author_a.id, 
            'publication_year': 2025
        }
        response = self.client.post(self.create_url, data, format='json')
        # Should be forbidden for POST (IsAuthenticatedOrReadOnly)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book_regular_user_fails(self):
        """Ensure non-staff users (regular_user) are blocked from updates."""
        self.client.force_authenticate(user=self.regular_user)
        updated_data = {
            'title': 'Foundation Updated',
            'author': self.author_a.id,
            'publication_year': 2000, 
            'isbn': self.book1.isbn
        }
        response = self.client.put(self.update_url, updated_data, format='json')
        # Should be forbidden because permissions are set to IsAuthenticatedOrReadOnly 
        # and we are using generic views which require global permissions for update.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_unauthenticated_fails(self):
        """Ensure unauthenticated users are blocked from deletion."""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)


    # --- 3. Filtering, Searching, and Ordering Tests (Task 2 verification) ---

    def test_filtering_by_publication_year(self):
        """Ensure filtering by publication_year works correctly."""
        # Query: Get books published in 1954
        response = self.client.get(self.list_url, {'publication_year': 1954})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "The Caves of Steel")

    def test_searching_by_title_keyword(self):
        """Ensure searching by keyword in the title works correctly."""
        # Query: Search for 'Hand' (should find 'The Left Hand of Darkness')
        response = self.client.get(self.list_url, {'search': 'Hand'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "The Left Hand of Darkness")

    def test_ordering_by_title_descending(self):
        """Ensure ordering by title in descending order works correctly."""
        # Query: Order by -title (Z to A)
        response = self.client.get(self.list_url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Expected order (Descending title):
        # 1. The Left Hand of Darkness
        # 2. The Caves of Steel
        # 3. Foundation
        self.assertEqual(response.data[0]['title'], "The Left Hand of Darkness")
        self.assertEqual(response.data[2]['title'], "Foundation")