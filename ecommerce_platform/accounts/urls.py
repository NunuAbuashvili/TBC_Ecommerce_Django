from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', views.user_logout, name='logout'),
]
