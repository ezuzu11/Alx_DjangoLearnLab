from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import list_books, LibraryDetailView
# Implementing Custom Permissions
from .views import add_book, edit_book, delete_book

urlpatterns = [
    path('books/', list_books, name='list_books'),  # Function-based view URL
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view URL
    # Implementation User Authentication 
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # Role-Based Access Control 
    path('Admin/', views.admin_view, name='admin_view'),
    path('Librarians/', views.librarian_view, name='librarian_view'),
    path('Member/', views.member_view, name='member_view'),

    # Implementing Custom Permissions
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:book_id>/', edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', delete_book, name='delete_book'),

]
