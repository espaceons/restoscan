# accounts/context_processors.py
from commandes.models import Commande
from tables.models import Table
from django.contrib.auth import get_user_model

User = get_user_model()

def restaurant_stats(request):
    if not request.user.is_authenticated:
        return {}

    # Calcul des statistiques
    total_commandes = Commande.objects.count()
    
    # Tables ayant au moins une commande active
    tables_occupees = Table.objects.filter(
        commandes__statut__in=['en_attente', 'en_preparation', 'prete']
    ).distinct().count()
    
    # utilisation de 'commandes_gerees' au lieu de 'commandes'
    serveurs_actifs = User.objects.filter(
        role='serveur', 
        commandes_gerees__isnull=False
    ).distinct().count()
    
    # Récupérer les serveurs et leurs commandes pour la rubrique détaillée
    serveurs_stats = User.objects.filter(role='serveur').prefetch_related('commandes_gerees')

    return {
        'stat_commandes': total_commandes,
        'stat_tables_occupees': tables_occupees,
        'stat_serveurs': serveurs_actifs,
        'serveurs_stats': serveurs_stats,
    }