from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Alias for Django built-in views

urlpatterns= [
    path('', views.home, name=''),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('profile/', views.profile_view, name='profile'),
    path('services/', views.services_view, name='services'),
    path('company/',views.company,name='company'),
    path('facts/', views.facts, name='facts'),
    path('installation/', views.installation, name='installation'),

]
