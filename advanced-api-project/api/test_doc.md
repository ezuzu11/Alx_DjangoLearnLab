1. Imports and Setup

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Book, Author
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

Explanation:
reverse: This is used to generate URLs for testing. Rather than hardcoding URLs, we use reverse() to dynamically look up the correct URL for a given view.
status: DRF's module for HTTP status codes (e.g., HTTP_200_OK, HTTP_201_CREATED), which we will use to check responses from the API.
APITestCase: DRF's test case class, which provides tools to simulate API requests and test the responses.
Book, Author: These are the models we're testing in our API.
Token: DRF's token authentication system. We use tokens to authenticate requests to the API.
User: The built-in Django user model, used to simulate authenticated users.

2. Test Setup
def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='testpass')
    self.token = Token.objects.create(user=self.user)
    self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    self.author1 = Author.objects.create(name="Author One")
    self.book1 = Book.objects.create(title="Book One", publication_year=2000, author=self.author1)
    self.book2 = Book.objects.create(title="Book Two", publication_year=2010, author=self.author1)

Explanation:
setUp(self): This method runs before each test case. It sets up the initial data and authentication required for testing.
Creating a user: A test user (testuser) is created using Django's create_user() method. This user is used to authenticate API requests.
Token authentication: The Token.objects.create() method generates a token for the test user, which is then passed in the HTTP headers for API requests.
Creating test data: Two authors and two books are created to test API endpoints that retrieve, update, or delete these objects.


3. Test Case for Creating a Book
def test_create_book(self):
    data = {
        "title": "New Book",
        "publication_year": 2021,
        "author": self.author1.id
    }
    response = self.client.post(reverse('book-list'), data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Book.objects.count(), 3)

Explanation:
test_create_book(self): This method tests the API’s ability to create a new book.
Data: The data dictionary simulates the data a user would provide to create a book (title, publication year, author).
self.client.post(): Sends a POST request to the book-list endpoint (dynamically retrieved with reverse('book-list')). It creates a new book and expects the response to be in JSON format.
Assertions:
assertEqual(response.status_code, status.HTTP_201_CREATED): Verifies that the response status code is 201 Created, meaning the book was successfully created.
assertEqual(Book.objects.count(), 3): Checks that there are now 3 books in the database.

4. Test Case for Retrieving the Book List
def test_get_book_list(self):
    response = self.client.get(reverse('book-list'))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)

Explanation:
test_get_book_list(self): Tests the API’s ability to retrieve a list of all books.
self.client.get(): Sends a GET request to the book-list endpoint.
Assertions:
assertEqual(response.status_code, status.HTTP_200_OK): Verifies that the response status is 200 OK.
assertEqual(len(response.data), 2): Ensures that 2 books are returned in the response.


5. Test Case for Updating a Book
def test_update_book(self):
    data = {
        "title": "Updated Book",
        "publication_year": 2020,
        "author": self.author1.id
    }
    response = self.client.put(reverse('book-detail', kwargs={'pk': self.book1.pk}), data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.book1.refresh_from_db()
    self.assertEqual(self.book1.title, "Updated Book")


Explanation:
test_update_book(self): Tests updating an existing book.
Data: The data dictionary contains the updated book information (new title and publication year).
self.client.put(): Sends a PUT request to the book-detail endpoint for book1, updating its details.
Assertions:
assertEqual(response.status_code, status.HTTP_200_OK): Verifies that the response status is 200 OK, meaning the book was successfully updated.
self.book1.refresh_from_db(): Refreshes book1 from the database to check that its title was updated.
assertEqual(self.book1.title, "Updated Book"): Ensures the title is now "Updated Book".

6. Test Case for Deleting a Book
def test_delete_book(self):
    response = self.client.delete(reverse('book-detail', kwargs={'pk': self.book1.pk}))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Book.objects.count(), 1)

Explanation:
test_delete_book(self): Tests the API’s ability to delete a book.
self.client.delete(): Sends a DELETE request to the book-detail endpoint for book1.
Assertions:
assertEqual(response.status_code, status.HTTP_204_NO_CONTENT): Verifies that the response status is 204 No Content, indicating the book was successfully deleted.
assertEqual(Book.objects.count(), 1): Ensures that only 1 book remains in the database.


7. Test Case for Filtering Books by Author

def test_filter_books_by_author(self):
    response = self.client.get(reverse('book-list'), {'author': self.author1.id})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)


Explanation:
test_filter_books_by_author(self): Tests the API’s filtering capability to return books by a specific author.
self.client.get(): Sends a GET request to the book-list endpoint, passing the author ID as a query parameter.
Assertions:
assertEqual(response.status_code, status.HTTP_200_OK): Verifies that the request is successful.
assertEqual(len(response.data), 2): Ensures that both books by author1 are returned.


8. Test Case for Searching Books

def test_search_books(self):
    response = self.client.get(reverse('book-list'), {'search': 'Book One'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)


Explanation:
test_search_books(self): Tests the search functionality by querying books with "Book One" in the title.
self.client.get(): Sends a GET request with a search query.
Assertions:
assertEqual(response.status_code, status.HTTP_200_OK): Ensures the search request is successful.
assertEqual(len(response.data), 1): Checks that only 1 book matches the search query.


9. Test Case for Ordering Books by Publication Year

def test_order_books_by_publication_year(self):
    response = self.client.get(reverse('book-list'), {'ordering': 'publication_year'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data[0]['title'], 'Book One')
    self.assertEqual(response.data[1]['title'], 'Book Two')

    
Explanation:
test_order_books_by_publication_year(self): Tests if books can be ordered by their publication year.
self.client.get(): Sends a GET request with the ordering query parameter.
Assertions:
assertEqual(response.status_code, status.HTTP_200_OK): Ensures the request is successful.
Checks order: Ensures that the books are ordered correctly by publication year.