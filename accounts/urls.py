# accounts/urls.py
from django.urls import path
from .views import (
    admin_dashboard,
    home_view,
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    UserListView,
    UserUpdateView,
    toggle_user_status,
)

app_name = 'accounts'

urlpatterns = [
    path('', home_view, name='home'),  # <-- La page d'accueil globale
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/toggle/', toggle_user_status, name='user_toggle'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
]