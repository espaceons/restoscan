# tables/urls.py
from django.urls import path
from .views import (
    TableListView,
    TableCreateView,
    TableUpdateView,
    toggle_table_status,
    serveur_dashboard,
)

app_name = 'tables'

urlpatterns = [
    path('', TableListView.as_view(), name='table_list'),
    path('add/', TableCreateView.as_view(), name='table_add'),
    path('<int:pk>/edit/', TableUpdateView.as_view(), name='table_edit'),
    path('<int:pk>/toggle/', toggle_table_status, name='table_toggle'),
    path('dashboard/', serveur_dashboard, name='serveur_dashboard'),
]