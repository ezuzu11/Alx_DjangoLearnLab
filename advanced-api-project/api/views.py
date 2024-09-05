from django.shortcuts import render
from rest_framework import generics, filters
from .models import Book
from .seriealizers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter

# Create your views here.

#ListView getting all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author_name', 'publication_year']
    search_fields = ['title', 'author_name']
    ordering_fields = ['title', 'author_name']
    ordering = ['title']
    permission_class = [IsAuthenticatedOrReadOnly]

# DetailView getting a single book by its ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_class = [IsAuthenticatedOrReadOnly] 


# CreateView Add a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_class = [IsAuthenticated]#OrReadOnly]

# UpdateView simply updating an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_class = [IsAuthenticated]#OrReadOnly]


# DeleteView deleting a book   
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_class = [IsAuthenticated]#OrReadOnly]
