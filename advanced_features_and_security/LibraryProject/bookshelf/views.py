from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Article
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def view_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'view_article.html', {'article': article})

@permission_required('bookshelf.can_create', raise_exception=True)
def create_article(request):
    # Logic to create an article
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # Logic to edit the article
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # Logic to delete the article
    pass

def book_list(request):
    books = Book.objects.all()  # Retrieve all books from the database
    return render(request, 'bookshelf/book_list.html', {'books': books})