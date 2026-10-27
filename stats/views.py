# stats/views.py
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import redirect, render
from django.utils import timezone
from commandes.models import Commande, LigneCommande
from menu.models import Plat
from tables.models import Table

User = get_user_model()


@login_required
def stats_dashboard_view(request):
  if not request.user.is_superuser and getattr(request.user, 'role', '') != 'admin':
    return redirect('accounts:home')

  periode = request.GET.get('periode', 'all')
  maintenant = timezone.now()

  commandes_qs = Commande.objects.all()

  # 🔍 utilisation de 'date_creation' au lieu de 'date'
  if periode == 'today':
    commandes_qs = commandes_qs.filter(date_creation__date=maintenant.date())
  elif periode == 'week':
    debut_semaine = maintenant - timedelta(days=7)
    commandes_qs = commandes_qs.filter(date_creation__gte=debut_semaine)
  elif periode == 'month':
    debut_mois = maintenant - timedelta(days=30)
    commandes_qs = commandes_qs.filter(date_creation__gte=debut_mois)

  total_commandes = commandes_qs.count()
  commandes_en_cours = commandes_qs.exclude(statut='servie').count()

  total_tables = Table.objects.count()
  tables_occupees_ids = (
      commandes_qs.filter(
          statut__in=['en_attente', 'en_preparation', 'prete']
      )
      .values_list('table_id', flat=True)
      .distinct()
  )
  tables_occupees_count = Table.objects.filter(
      id__in=tables_occupees_ids
  ).count()
  tables_libres_count = total_tables - tables_occupees_count
  taux_occupation = (
      round((tables_occupees_count / total_tables) * 100, 1)
      if total_tables > 0
      else 0
  )

  tables_populaires = (
      Table.objects.filter(commandes__in=commandes_qs)
      .annotate(total_commandes_table=Count('commandes'))
      .order_by('-total_commandes_table')[:5]
  )

  plats_populaires = (
      Plat.objects.filter(lignecommande__commande__in=commandes_qs)
      .annotate(total_vendu=Sum('lignecommande__quantite'))
      .filter(total_vendu__isnull=False)
      .order_by('-total_vendu')[:5]
  )

  serveurs_stats = User.objects.filter(role='serveur').prefetch_related(
      'commandes_gerees'
  )

  context = {
      'total_commandes': total_commandes,
      'commandes_en_cours': commandes_en_cours,
      'tables_occupees': tables_occupees_count,
      'total_tables': total_tables,
      'tables_libres': tables_libres_count,
      'taux_occupation': taux_occupation,
      'tables_populaires': tables_populaires,
      'plats_populaires': plats_populaires,
      'serveurs_stats': serveurs_stats,
      'periode_actuelle': periode,
  }

  return render(request, 'stats/stats_dashboard.html', context)