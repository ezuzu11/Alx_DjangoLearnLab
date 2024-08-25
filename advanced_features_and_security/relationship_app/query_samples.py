from relationship_app.models import Author, Book, Librarian, Library

#query 1: Query all books by a specific author
def query_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    #books = author.books.all()
    books = Book.objects.filter(author=author)
    return books

#query 2: List all books in a library
def query_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    return books

# Query 3: Retrieve the librarian for a library
def query_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    librarian = library.librarian  # Use related_name 'librarian'
    return librarian