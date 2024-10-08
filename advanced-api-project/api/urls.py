from django.urls import path
from .views import BookCreateView, BookDeleteView, BookDetailView, BookListView, BookUpdateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookListView)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('books/create', BookCreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>', BookListView.as_view(), name='book-delete'),

]