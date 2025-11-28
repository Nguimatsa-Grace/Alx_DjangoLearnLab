from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book 
from django.urls import reverse
from django.utils import timezone 

# --- URL NAMES CONFIRMED FROM USER'S urls.py ---
# book-list: GET /books/ (List, Search, Filter, Order)
# book-detail: GET, PUT, PATCH, DELETE /books/<int:pk>/ (Detail/Modify)
# ---

class AuthorAPITestCase(APITestCase):
    """
    Tests for the AuthorViewSet. Ensures basic CRUD operations and permissions.
    """
    def setUp(self):
        # Create user and author
        self.staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        self.author = Author.objects.create(name="H. G. Wells")
        
        self.list_url = reverse('author-list') 
        self.detail_url = reverse('author-detail', args=[self.author.id]) 

    def test_author_list_read_only(self):
        """Ensure unauthenticated users can view the list of authors (GET 200)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_create_authenticated(self):
        """Ensure only staff users can create an author (POST 201)."""
        self.client.force_authenticate(user=self.staff_user)
        data = {'name': 'Jules Verne'} 
        
        response = self.client.post(self.list_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_author_delete_unauthenticated_fails(self):
        """Ensure unauthenticated users cannot delete an author (DELETE 401/403)."""
        response = self.client.delete(self.detail_url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])


class BookAPITestCase(APITestCase):
    """
    Comprehensive unit tests for the Book API views.
    Checks are adjusted to handle non-paginated list responses (direct array).
    """
    def setUp(self):
        # 1. Create Users for Permission Testing
        self.staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        self.regular_user = User.objects.create_user(username='regularuser', password='password123')

        # 2. Create Authors
        self.author_a = Author.objects.create(name="Isaac Asimov")
        self.author_b = Author.objects.create(name="Ursula K. Le Guin")
        
        # 3. Create Books
        self.book1 = Book.objects.create(
            title="Foundation", 
            author=self.author_a, 
            publication_year=1951,
        )
        self.book2 = Book.objects.create(
            title="The Caves of Steel", 
            author=self.author_a, 
            publication_year=1954,
        )
        self.book3 = Book.objects.create(
            title="The Left Hand of Darkness", 
            author=self.author_b, 
            publication_year=1969,
        )

        # 4. URLs
        self.list_url = reverse('book-list')           # GET and POST (now combined)
        # Note: No separate create_url needed, as POST goes to list_url
        self.detail_url = reverse('book-detail', args=[self.book1.id]) # GET, PUT, PATCH, DELETE

        # Payload structure for POST requests
        self.new_book_data = {
            'title': 'The Robots of Dawn',
            'author': self.author_a.id,
            'publication_year': 1983,
        }
        
        self.current_year = timezone.now().year


    # --- 1. CRUD Tests (Staff User) ---

    def test_list_books_unauthenticated_returns_200(self):
        """
        Ensure all users (unauthenticated) can view the list of books (GET 200).
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the response data is a list and contains 3 items
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book_unauthenticated_returns_200(self):
        """Ensure all users (unauthenticated) can retrieve book detail (GET 200)."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_staff_user_returns_201(self):
        """Ensure staff user can create a new book (POST 201 to the list URL)."""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(self.list_url, self.new_book_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_update_book_staff_user_returns_200(self):
        """Ensure staff user can update an existing book (PUT 200)."""
        self.client.force_authenticate(user=self.staff_user)
        updated_title = 'Foundation Updated'
        updated_data = {
            'title': updated_title,
            'author': self.author_a.id,
            'publication_year': self.book1.publication_year, 
        }
        response = self.client.put(self.detail_url, updated_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, updated_title)

    def test_delete_book_staff_user_returns_204(self):
        """Ensure staff user can delete a book (DELETE 204)."""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2) 


    # --- 2. Permission Tests (Non-Staff User) ---

    def test_create_book_regular_user_fails_returns_403(self):
        """Ensure regular authenticated user is blocked from creation (POST 403 to the list URL)."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.list_url, self.new_book_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
        
    def test_update_book_unauthenticated_fails_returns_401(self):
        """Ensure unauthenticated users are blocked from updates (PUT 401/403)."""
        updated_data = {
            'title': 'Attempted Hack',
            'author': self.author_a.id,
            'publication_year': self.book1.publication_year,
        }
        response = self.client.put(self.detail_url, updated_data, content_type='application/json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
    def test_delete_book_regular_user_fails_returns_403(self):
        """Ensure regular authenticated users are blocked from deletion (DELETE 403)."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # --- 3. Custom Validation Test (400 Bad Request) ---

    def test_create_book_with_future_year_fails_returns_400(self):
        """Test the custom validation that blocks publication years in the future (400)."""
        self.client.force_authenticate(user=self.staff_user)
        future_year_data = {
            'title': 'Yet To Be Published',
            'author': self.author_a.id,
            'publication_year': self.current_year + 1, # Future year
        }
        
        response = self.client.post(self.list_url, future_year_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Check that the specific error message for validation is returned
        expected_error_message = f"Publication year cannot be in the future. Current year is {self.current_year}."
        self.assertIn('publication_year', response.data)
        self.assertEqual(response.data['publication_year'][0], expected_error_message)


    # --- 4. Filtering, Searching, and Ordering Tests (BookListAPIView) ---

    def test_filtering_by_publication_year_returns_correct_count(self):
        """Ensure filtering by publication_year works correctly (GET 200)."""
        response = self.client.get(self.list_url, {'publication_year': 1954})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check data length directly
        self.assertEqual(len(response.data), 1) 

    def test_searching_by_title_keyword_returns_correct_book(self):
        """Ensure searching by keyword in the title works correctly (GET 200)."""
        response = self.client.get(self.list_url, {'search': 'Darkness'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check data length and content directly
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "The Left Hand of Darkness")

    def test_ordering_by_title_descending_is_correct(self):
        """Ensure ordering by title in descending order works correctly (GET 200)."""
        response = self.client.get(self.list_url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check data length and content directly
        self.assertEqual(response.data[0]['title'], "The Left Hand of Darkness")
        self.assertEqual(len(response.data), 3)