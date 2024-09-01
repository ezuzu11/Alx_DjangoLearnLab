from django.urls import path ,include
from rest_framework.routers import DefaultRouter
from .views import BookList
from .views import BookViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books', BookViewSet)  # Register the BookViewSet

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Map /books/ URL to the BookList view
    path('', include(router.urls)),  # Include the router's URL patterns
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
]
