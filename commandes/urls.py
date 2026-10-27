# commandes/urls.py
from django.urls import path
from .views import (
    CommandeCreateView,
    CommandeListView,
    cuisine_dashboard,
    update_commande_status,
)

app_name = 'commandes'

urlpatterns = [
    path('', CommandeListView.as_view(), name='commande_list'),
    path('add/', CommandeCreateView.as_view(), name='commande_add'),
    path('cuisine/', cuisine_dashboard, name='cuisine_dashboard'),

    # 🛠️ Couverture de tous les noms de routes possibles pour éviter le NoReverseMatch
    path('<int:pk>/status/<str:statut>/', update_commande_status, name='update_commande_status', ),
    path('<int:pk>/status/<str:statut>/', update_commande_status, name='update_status', ),
    path('<int:pk>/status/<str:statut>/', update_commande_status, name='changer_statut', ),
]