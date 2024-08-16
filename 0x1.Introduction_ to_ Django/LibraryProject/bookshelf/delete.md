# Delete Operation

### Command:
```python
from bookshelf.models import Book
book.delete()
 
#Expected Output:
'''python
books = Book.objects.all()
print(list(books))  # Should return an empty list: []

[]