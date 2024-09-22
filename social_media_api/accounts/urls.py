from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    #path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('login/', obtain_auth_token, name='api_token_auth'),
]
