from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='list_books'),  # Function-based view URL
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view URL
    # Implementation User Authentication 
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]
