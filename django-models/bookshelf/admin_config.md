# Django Admin Configuration for the Book Model

### Step 1: Register the Book Model
- Open `bookshelf/admin.py` and register the `Book` model:
```python
from django.contrib import admin
from .models import Book

admin.site.register(Book)

# Customize the Admin Interface

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',) # In Python, a single value inside a tuple or list must have a comma after it to differentiate it from just a plain value.
