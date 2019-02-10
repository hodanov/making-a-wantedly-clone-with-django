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
    path('users/<uuid:id>/', views.profile, name='profile'),
    path('user/profile/edit/', views.profile_edit, name='profile_edit'),
    path('user/profile/edit/post/', views.profile_edit_post, name='profile_edit_post'),
    path('orgs/<uuid:id>/', views.organization, name='organization'),
]

# To serve files uploaded by a user during development
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
