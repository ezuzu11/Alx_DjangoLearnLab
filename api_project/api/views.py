from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Create your views here.

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()  # Retrieve all Book instances
    serializer_class = BookSerializer  # Use the BookSerializer to serialize the data

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions 
    (list, create, retrieve, update, destroy) for the Book model.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer