from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('photo//', views.photo_detail, name='photo_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('photo//interact/', views.interact_photo, name='interact_photo'),
]