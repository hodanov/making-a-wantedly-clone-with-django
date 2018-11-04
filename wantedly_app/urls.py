from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user/profile/edit/', views.profile_edit, name='profile_edit'),
    # path('users/xxxxxxxxxx', views.profile_show, name='profile_show'),
    path('api/user/', views.UserListCreate.as_view() ),
]
