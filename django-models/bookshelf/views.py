from django.shortcuts import render, redirect
"""
# Implementing Custom Permissions
from django.contrib.auth.decorators import permission_required
from .models import Book, Author
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
# Create your views here.

#Add book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')
        author = Author.objects.get(id=author_id)

        # Create and save the book
        book = Book.objects.create(title=title, author=author)
        return redirect('book_list')  # Assuming you have a view that lists books

    # If GET, render the form (you'll need to create an HTML form to add books)
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})

# Update book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_id = request.POST.get('author_id')
        book.author = get_object_or_404(Author, id=author_id)
        book.save()
        return redirect('book_list')  # Redirect to the book list view

    authors = Author.objects.all()
    return render(request, 'relationship_app/update_book.html', {'book': book, 'authors': authors})


# delete book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Redirect to the book list view

    return render(request, 'relationship_app/confirm_delete.html', {'book': book})
"""