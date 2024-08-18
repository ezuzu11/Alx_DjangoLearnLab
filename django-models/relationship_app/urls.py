from django.urls import path
from . import views
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='list_books'),  # Function-based view URL
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view URL
]
