from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Book, Author
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a user and author for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Log in the user
        self.client.login(username= 'testuser', password= 'testpass')
        
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.author1 = Author.objects.create(name="Author One")
        self.book1 = Book.objects.create(title="Book One", publication_year=2000, author=self.author1)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2010, author=self.author1)

    def test_create_book(self):
        # Test creating a book
        data = {
            "title": "New Book",
            "publication_year": 2021,
            "author": self.author1.id
        }
        response = self.client.post(reverse('book-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_get_book_list(self):
        # Test retrieving a list of books
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_book(self):
        # Test updating a book
        data = {
            "title": "Updated Book",
            "publication_year": 2020,
            "author": self.author1.id
        }
        response = self.client.put(reverse('book-detail', kwargs={'pk': self.book1.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")

    def test_delete_book(self):
        # Test deleting a book
        response = self.client.delete(reverse('book-detail', kwargs={'pk': self.book1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_author(self):
        # Test filtering books by author
        response = self.client.get(reverse('book-list'), {'author': self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_books(self):
        # Test searching books by title
        response = self.client.get(reverse('book-list'), {'search': 'Book One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_publication_year(self):
        # Test ordering books by publication year
        response = self.client.get(reverse('book-list'), {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Book One')  # First book should be 'Book One'
        self.assertEqual(response.data[1]['title'], 'Book Two')
