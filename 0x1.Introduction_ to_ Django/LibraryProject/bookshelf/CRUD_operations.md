# Create Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# Expected Output:
<Book: 1984>

# Retrieve Operation
```python
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)

#Expected Output:
1984 George Orwell 1949

# Update Operation

### Command:
```python
book.title = "Nineteen Eighty-Four"
book.save()
 
#Expected Output:
print(book.title, book.author, book.publication_year)
Nineteen Eighty-Four George Orwell 1949

# Delete Operation

### Command:
```python
book.delete()
 
#Expected Output:
'''python
books = Book.objects.all()
print(list(books))  # Should return an empty list: []

[]
