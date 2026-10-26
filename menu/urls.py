# menu/urls.py
from django.urls import path
from .views import (
    CategorieListView,
    CategorieCreateView,
    CategorieUpdateView,
    CategorieDeleteView,
    PlatListView,
    PlatCreateView,
    PlatUpdateView,
    PlatDeleteView,
    toggle_plat_status,
)

app_name = 'menu'

urlpatterns = [
    path('categories/', CategorieListView.as_view(), name='categorie_list'),
    path('categories/add/', CategorieCreateView.as_view(), name='categorie_add'),
    path('categories/<int:pk>/edit/', CategorieUpdateView.as_view(),
         name='categorie_edit'),  # Route de modification
    path('categories/<int:pk>/delete/', CategorieDeleteView.as_view(),
         name='categorie_delete'),  # Route de suppression
    path('', PlatListView.as_view(), name='plat_list'),
    path('plats/add/', PlatCreateView.as_view(), name='plat_add'),
    path('plats/<int:pk>/edit/', PlatUpdateView.as_view(), name='plat_edit'),
    path('plats/<int:pk>/delete/', PlatDeleteView.as_view(), name='plat_delete'),
    path('plats/<int:pk>/toggle/', toggle_plat_status, name='plat_toggle'),
]
