from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    #path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('login/', obtain_auth_token, name='api_token_auth'),

    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]
