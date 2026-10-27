# commandes/views.py
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from menu.models import Plat
from tables.models import Table
from .models import Commande, LigneCommande
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


from .models import Commande

@login_required
def cuisine_dashboard(request):
    # Le cuisinier a besoin de voir les commandes en attente et en préparation
    commandes = Commande.objects.filter(
        statut__in=['en_attente', 'en_preparation']).order_by('date_creation')
    return render(request, 'commandes/cuisine_dashboard.html', {'commandes': commandes})


# commandes/views.py
@method_decorator(login_required, name='dispatch')
class CommandeCreateView(View):

    def get(self, request):
        user = request.user
        # Si c'est un admin, il voit toutes les tables. Si c'est un serveur, il ne voit que ses tables.
        if user.is_superuser or getattr(user, 'role', '') == 'admin':
            tables = Table.objects.all()
        else:
            tables = Table.objects.filter(serveur=user)

        plats = Plat.objects.filter(disponible_du_jour=True)

        return render(
            request,
            'commandes/commande_form.html',
            {'tables': tables, 'plats': plats}
        )

    def post(self, request):
        table_id = request.POST.get('table')
        table = get_object_or_404(Table, pk=table_id)

        # 🎯 Le serveur de la commande devient automatiquement le serveur assigné à cette table !
        # Si aucun serveur n'est assigné à la table, on prend l'utilisateur connecté par défaut (ex: l'admin).
        serveur_commande = table.serveur if table.serveur else request.user

        # 1. Créer la commande principale
        commande = Commande.objects.create(
            table=table,
            serveur=serveur_commande,
            statut='en_attente'
        )

        # 2. Récupérer les plats et quantités soumis depuis le formulaire
        for key, value in request.POST.items():
            if key.startswith('plat_') and int(value) > 0:
                plat_id = key.split('_')[1]
                plat = get_object_or_404(Plat, pk=plat_id)
                quantite = int(value)

                LigneCommande.objects.create(
                    commande=commande,
                    plat=plat,
                    quantite=quantite
                )

        return redirect('commandes:commande_list')




@method_decorator(login_required, name='dispatch')
class CommandeListView(ListView):
    model = Commande
    template_name = 'commandes/commande_list.html'
    context_object_name = 'commandes'
    ordering = ['-date_creation']

    def get_queryset(self):
        user = self.request.user

        # 1. Si c'est un admin ou superuser, il voit TOUTES les commandes
        if user.is_superuser or getattr(user, 'role', '') == 'admin':
            return Commande.objects.all()

        # 2. Si c'est un serveur, il voit ses commandes OU les commandes de ses tables assignées
        elif getattr(user, 'role', '') == 'serveur':
            return Commande.objects.filter(
                Q(serveur=user) | Q(table__serveur=user)
            ).distinct()

        # 3. Pour la cuisine ou autres rôles, ils voient les commandes en cours ou selon besoin
        elif getattr(user, 'role', '') == 'cuisine':
            return Commande.objects.filter(statut__in=['en_attente', 'en_preparation', 'prete'])

        # Par sécurité par défaut
        return Commande.objects.none()




@login_required
def update_commande_status(request, pk, statut):
    commande = get_object_or_404(Commande, pk=pk)

    # 🔍 Vérification : est-ce que le statut envoyé fait partie des choix autorisés ?
    # ou ['en_attente', 'en_preparation', 'prete', 'servie', 'annulee', 'payee']
    valid_statuts = [dict(Commande.STATUT_CHOICES).keys()]

    if statut in ['en_attente', 'en_preparation', 'prete', 'servie', 'annulee', 'payee']:
        commande.statut = statut
        commande.save()

        # Optionnel : si la commande est payée, on peut libérer la table ou changer son état
        if statut == 'payee':
            # (selon votre champ dans le modèle Table)
            commande.table.est_occupee = False
            commande.table.save()

    # Redirection selon le rôle ou vers la page précédente
    if request.user.role == 'cuisine':
        return redirect('commandes:cuisine_dashboard')
    return redirect('commandes:commande_list')


@login_required
def marquer_payee(request, pk):
  """Permet de marquer une commande comme payée, ce qui libère la table"""
  commande = get_object_or_404(Commande, pk=pk)

  # Mettre à jour le statut à 'payee'
  commande.statut = 'payee'
  commande.save()

  return redirect('commandes:commande_list')
