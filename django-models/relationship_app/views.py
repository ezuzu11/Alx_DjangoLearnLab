from django.shortcuts import render
from .models import Book
from django.views.generic.detail import DetailView
from .models import Library
# Create your views here.

#Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'templates/relationship_app/list_books.html', {'books': books})

# Class-based view for displaying library details
class LibraryDetailView(DetailView):
    model = Library  # Specify the model
    template_name = 'templates/relationship_app/library_detail.html'  # Template to use
    context_object_name = 'library'  # Context variable name